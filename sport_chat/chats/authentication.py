from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = request.GET.get('token')

        if not key:
            raise exceptions.AuthenticationFailed('No such token')       
                    
        try:
            token = Token.objects.get(key=key)
            user = authenticate(username=token.username, password=token.password)
        except:
            raise exceptions.AuthenticationFailed('Authentication Failed')
        
        return (user, None)