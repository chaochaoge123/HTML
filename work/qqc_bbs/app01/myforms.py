from django import forms
from django.forms import widgets
from django.core.exceptions import  ValidationError
from app01 import models
class RegForms(forms.Form):
    name=forms.CharField (max_length= 10,min_length= 2,label='用户名',
                          error_messages= {'required':'该字段必填','max_length':'太长了'},
                          widget=widgets .TextInput(attrs={'class': 'form-control'}))
    pwd=forms.CharField (min_length= 5,label= '密码',
                         error_messages= {'required':'改字段必填','min_length':'太短了'},
                         widget=widgets .PasswordInput(attrs={'class': 'form-control'}))
    re_pwd=forms.CharField (min_length= 5,label= '确认密码',
                         error_messages= {'required':'改字段必填','min_length':'太短了'},
                         widget=widgets .PasswordInput(attrs={'class': 'form-control'}))

    email=forms.EmailField (label='邮箱',
                            error_messages= {'required':'改字段必填','invalid':'不是邮箱格式'},
                            widget= widgets .EmailInput (attrs={'class': 'form-control'}))

    def clean_name(self):
        name=self.cleaned_data.get('name')
        user=models.UserInfo.objects.filter(username=name)
        if user:
            raise ValidationError ('用户已存在')
        else:
            return name

    def clean(self):
        pwd=self.cleaned_data.get('pwd')
        re_pwd=self.cleaned_data.get('re_pwd')
        if pwd and re_pwd :
            if pwd==re_pwd :
                return self.cleaned_data
            else:
                raise ValidationError ('密码不一致')


































