from rest_framework .authentication import  BaseAuthentication
from rest_framework.exceptions import  AuthenticationFailed
from app01 import models
class TokenAuth():
    def authenticate(self,request):
        token=request .GET.get('token')
        token_obj=models.UserToken .objects .filter(token=token).first()
        if token_obj:
            return token_obj.user,token_obj
        else:
            raise AuthenticationFailed ('认证失败')

    def authenticate_header(self,request):
        pass












































