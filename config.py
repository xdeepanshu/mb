
#JWT CONFIGURATION SETTINGS 

# https://jpadilla.github.io/django-rest-framework-jwt/

JWT_EXPIRATION_DELTA_IN_SEC = 24 * 60 * 60 # 1 day
JWT_ALLOW_REFRESH = True
JWT_REFRESH_EXPIRATION_DELTA = 24 * 60 * 60 # 1 day
JWT_AUTH_HEADER_PREFIX = 'Bearer'


#Use JWT 
REST_USE_JWT = True

#Using our custom user model
AUTH_USER_MODEL = 'user.CustomUser'


# More about the settings here https://djoser.readthedocs.io/en/latest/settings.htm
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL' : True,
    'SEND_CONFIRMATION_EMAIL' : True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION' : True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION' : True,
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'LOGOUT_ON_PASSWORD_CHANGE'  : True, 

}
