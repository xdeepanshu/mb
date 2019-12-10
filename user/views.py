from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from rest_framework import generics, status, request
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import permission_classes, api_view

from user.models import CustomUser
from user.serializers import UserCreateSerializer, UserSerializer
from user.tokens import account_activation_token

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema


#Private view, you need to be authenticated before
class User(APIView):

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["terms_and_condition"] is False:
            data = {
                "error" : "Please accept the terms and condtions"
            }
            raise ValidationError(data)
        #Hash the password
        user = serializer.save(is_active=False, password=make_password(serializer.validated_data["password"]))

        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        data = {
            "user_details" : serializer.data, 
            "message" : "A confirmation email has been sent on %s"%(user.email),
        }
        return Response(data=data)
    
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user for user in CustomUser.objects.all()]
        serializer = UserSerializer(usernames, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        """
        Delete deletes a user of a given id or it deletes the current user if the id parameter is not provided.
        """
        data = {}
        try:
            if request.data.__contains__('id'):
                user = CustomUser.objects.get(pk=request.data['id'])
            else :
                user = CustomUser.objects.get(pk=request.user.id)
            user.delete()
            data['status'] = 'Account of username %s has been deleted successfully'%user.username
            return Response(data=data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist as e:
            data['error'] = "The user of the given id doesn't exist."
        except Exception as e:
            data['error'] = str(e)
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):

        """
        Updates the parameters of the user 
        """
        try:
            data = request.data.copy() #Request.data is immutable
            user = CustomUser.objects.get(pk=request.user.id)
            if not data.__contains__("username"):
                data["username"] = getattr(user, "username")    
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                data['error'] = serializer.errors
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            data = {}
            data["error"] = "Sorry but you don't exist"
            raise ValidationError(data)

@api_view(http_method_names=['GET'])
@permission_classes((AllowAny,))
def activate(request, uidb64, token):
    data = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        #return redirect('home')
        data["message"] = 'Thank you for your email confirmation. Now you can login your account.'
        return Response(data=data, status = status.HTTP_200_OK)
    else:
        data["error"]="Either the activation link is invalid or the user email is already verified."
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
 
    
