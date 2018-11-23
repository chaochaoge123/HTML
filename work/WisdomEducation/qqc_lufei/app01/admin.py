from django.contrib import admin

from app01 import models
admin.site.register(models.Course )
admin.site.register(models.CourseDetail)
admin.site.register(models.PricePolicy)
admin.site.register(models.Teacher)