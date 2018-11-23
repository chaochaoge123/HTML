from django.shortcuts import render,HttpResponse
from rest_framework .views import APIView
from rest_framework .response import  Response
from app01 import models
from app01.utils.commonUtils import *
from app01.ser import *
from rest_framework.viewsets import  ViewSetMixin

class Course(ViewSetMixin,APIView ):
    def get_all(self,request):
        myret=MyResponse()
        ret=models.Course .objects .all()
        ser=CourseSer(instance= ret,many=True )
        myret.msg='获取成功'
        myret.data=ser.data # 将信息放到字典里
        return Response (myret.get_dic())

        # return Response (['python','linux'])

    def get_one(self,request,pk):
        myret=MyResponse ()
        ret =models.CourseDetail.objects.filter(course_id=pk) .first()
        ser=CourseDetailSer(instance= ret,many= False )
        myret.msg='查询成功'
        myret.data=ser.data
        return Response (myret.get_dic())


















