
from rest_framework .views import APIView
from rest_framework .response import  Response
from app01.utils .commonUtils import  MyResponse
from app01.models import *
from django.core.exceptions import  ObjectDoesNotExist
import uuid
class Login(APIView ):
    def post(self,request):
        res=MyResponse ()
        try:
            name=request .data.get('name',None )
            pwd=request .data.get('pwd',None )
            user=User.objects .get(name=name,pwd=pwd)
            token=str(uuid.uuid4() )
            print(token)
            # 有就更新，没有就创建
            obj_token=UserToken.objects .update_or_create(user=user,defaults= {'token':token})
            res.name=name
            res.token=token
        except ObjectDoesNotExist as e:
            res.status=1001
            res.msg='用户名或者密码错误'
        except Exception as e:
            res.status=1001
            res.msg=str(e)
        return Response (res.get_dic() )


























