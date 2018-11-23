from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

# class Course(models.Model ):
#     name=models.CharField (max_length= 128,unique= True )
#     course_img=models.CharField (max_length= 255)
#     brief=models.TextField (verbose_name='课程概述',max_length= 2048)
#     level_choices=((0,'初级'),(1,'中级'),(2,'高级'))
#     level=models.SmallIntegerField (choices=level_choices ,default= 1)
#
#     pub_date=models.DateField (verbose_name= "发布日期",blank=True,null=True )
#     period=models.PositiveIntegerField (verbose_name= "建议学习周期(day)",default= 7)
#     order=models.IntegerField ("课程顺序",help_text= "从上一个课程数字往后排")
#
#     status_choices=((0, '上线'), (1, '下线'), (2, '预上线'))
#     status=models.SmallIntegerField (choices= status_choices,default= 0)
#     price_policy=GenericRelation ('PricePolicy')
#
#     def __str__(self):
#         return self .name
#
#     class Meta:
#         #显示表名为专题课
#         verbose_name_plural='专题课'
#
# class CourDetail(models.Model):
#     course=models.OneToOneField ('Course',on_delete= models.CASCADE)
#     hours=models.IntegerField ("课时")
#     # 课程标语
#     course_slogan=models.CharField (max_length= 125,blank=True ,null=True )
#
#     #推荐课程
#     #related_name 反向查询时表名_set 变为recommend_by
#     recommend_course=models.ManyToManyField ("Course",related_name= "recommend_by",blank=True )
#     teachers=models.ManyToManyField ("Teacher",verbose_name= '课程讲师')
#
#     def __str__(self):
#         return "%s" % self.course
#     class Meta:
#         verbose_name_plural ="课程详细"
#
# class PricePolicy(models.Model ): # 价格与课程周期表
#     content_type=models.ForeignKey (ContentType,on_delete= models.CASCADE)
#     object_id=models.PositiveIntegerField ()
#     content_object=GenericForeignKey (content_type,object_id)
#     valid_period_choices = ((1, '1天'), (3, '3天'),
#                             (7, '1周'), (14, '2周'),
#                             (30, '1个月'),
#                             (60, '2个月'),
#                             (90, '3个月'),
#                             (180, '6个月'), (210, '12个月'),
#                             (540, '18个月'), (720, '24个月'),
#                             )
#     valid_period=models.SmallIntegerField (choices= valid_period_choices )
#     price=models.FloatField ()
#
#     class Meta():
#         #联合唯一
#         unique_together =("content_type", 'object_id', "valid_period")
#         verbose_name_plural ="价格策略"
#
#     def __str__(self):
#          return "%s(%s)%s" % (self.content_object,self.get_valid_period_display(),self.price)
#
# class Teacher(models.Model ):
#     name=models.CharField (max_length= 32)
#     image=models.CharField (max_length= 128)
#     brief=models.TextField (max_length= 1024)
#
#     def __str__(self):
#         return self .name
#     class Meta():
#         verbose_name_plural = "讲师"


class User(models.Model ):
    name=models.CharField (max_length= 32)
    pwd=models.CharField (max_length= 32)
    type=models.IntegerField (choices=((1,"common"),(2,"VIP"),(3,"SVIP")),default= 1)
    bely=models.IntegerField ()
    def __str__(self):
        return self.name

class UserToken(models.Model):
    user=models.OneToOneField ("User")
    token=models.CharField (max_length= 128)


class Course(models.Model):
    """专题课程"""
    name = models.CharField(max_length=128, unique=True)
    course_img = models.CharField(max_length=255)
    # verbose_name 在admin后台显示为中文
    brief = models.TextField(verbose_name="课程概述", max_length=2048)

    level_choices = ((0, '初级'), (1, '中级'), (2, '高级'))
    level = models.SmallIntegerField(choices=level_choices, default=1)
    pub_date = models.DateField(verbose_name="发布日期", blank=True, null=True)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=7)
    order = models.IntegerField("课程顺序", help_text="从上一个课程数字往后排")

    status_choices = ((0, '上线'), (1, '下线'), (2, '预上线'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    price_policy = GenericRelation("PricePolicy")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "专题课"


class CourseDetail(models.Model):
    """课程详情页内容"""
    course = models.OneToOneField("Course", on_delete=models.CASCADE)
    hours = models.IntegerField("课时")
    # 课程的标语 口号
    course_slogan = models.CharField(max_length=125, blank=True, null=True)
    # video_brief_link = models.CharField(verbose_name='课程介绍', max_length=255, blank=True, null=True)
    # why_study = models.TextField(verbose_name="为什么学习这门课程")
    # what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
    # career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
    # prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    # 推荐课程
    recommend_courses = models.ManyToManyField("Course", related_name="recommend_by", blank=True)
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")

    def __str__(self):
        return "%s" % self.course

    class Meta:
        verbose_name_plural = "课程详细"



class PricePolicy(models.Model):
    """价格与有课程效期表"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 关联course or degree_course
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # course = models.ForeignKey("Course")
    valid_period_choices = ((1, '1天'), (3, '3天'),
                            (7, '1周'), (14, '2周'),
                            (30, '1个月'),
                            (60, '2个月'),
                            (90, '3个月'),
                            (180, '6个月'), (210, '12个月'),
                            (540, '18个月'), (720, '24个月'),
                            )
    valid_period = models.SmallIntegerField(choices=valid_period_choices)
    # obj.get_valid_period_display()
    price = models.FloatField()
    # django这门课1周    9.9
    # django这门课1周    19.9
    class Meta:
        unique_together = ("content_type", 'object_id', "valid_period")
        verbose_name_plural = "价格策略"

    def __str__(self):
        return "%s(%s)%s" % (self.content_object, self.get_valid_period_display(), self.price)

class Teacher(models.Model):
    """讲师、导师表"""
    name = models.CharField(max_length=32)
    image = models.CharField(max_length=128)
    brief = models.TextField(max_length=1024)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name_plural = "讲师"


