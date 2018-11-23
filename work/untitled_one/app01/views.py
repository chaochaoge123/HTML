from django.shortcuts import render
import json
from app01 import models
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from  app01. common import MyResponse

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'

class Book(APIView):
    def get(self, request):
        book_list = models.Book.objects.all()
        bs = BookSerializers(book_list, many=True)
        return Response(bs.data)

    def post(self, request):
        print(request.data)
        bs = BookSerializers(data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)

class Bookser(APIView ):
    def get(self,request,pk):
        book_obj=models.Book.objects .filter(title=pk).first()
        bs=BookSerializers (book_obj ,many=False )
        print(bs .data )
        return Response (bs.data)

    def put(self,request,pk):
        book_obj=models.Book.objects .filter(title=pk).first()
        ret=BookSerializers (data=request.data,instance= book_obj )
        if ret.is_valid() :
            ret.save()
            return Response (ret.data)
        else:
            return Response (ret.errors )

    def delete(self,request,pk):
        book_ibj=models.Book.objects .filter(title=pk) .delete()
        return Response ('删除成功')



class Tset(APIView):
    def get(self,request):
        res=MyResponse()
        # dic={'status':100,'timezone':None,'time':None}
        from django.utils import timezone
        from untitled_one import settings
        res.status=200
        res.time=timezone.localtime(timezone .now()).strftime('%Y-%m-%d %H:%M:%S')
        res.timezone=settings.TIME_ZONE
        res.msg='查询成功'

        return Response (res.get_dic())






