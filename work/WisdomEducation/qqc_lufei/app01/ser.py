from rest_framework import serializers
from app01 import models
class CourseSer(serializers .ModelSerializer ):
    class Meta:
        model=models.Course
        fields="__all__"

class CourseDetailSer(serializers.ModelSerializer ):
    class Meta:
        model=models.CourseDetail
        fields="__all__"
    name=serializers.CharField (source= 'course.name')
    teachers=serializers .SerializerMethodField ()
    def get_teachers(self,obj):
         return [i.name for i in obj.teachers.all()]

    # #推荐课程
    recommend_courses=serializers .SerializerMethodField ()
    def get_recommend_courses(self,obj):
         return [{'name':i.name,'id':i.id} for i in obj.recommend_courses.all()]
    #价格策略
    policy_price=serializers .SerializerMethodField ()
    def get_policy_price(self,obj):
        ret=obj.course.price_policy.all()  # 所有价格策略
        # 返回ID，价格周期，价格
        return [{'id': price.id, 'valid_period': price.get_valid_period_display(), 'price': price.price} for price in
                ret]















