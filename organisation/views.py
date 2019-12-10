from rest_framework.views import APIView
from organisation.serializer import OrganisationSerializer
from rest_framework.decorators import permission_classes
from organisation.models import Organisation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class OrganisationView(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    
    def get(self, request, format=None):
        #It will only return one object
        organisations = [organisation for organisation in Organisation.objects.all()]
        serilizer = OrganisationSerializer(organisations, many=True)
        return Response(serilizer.data, status=status.HTTP_200_OK)
