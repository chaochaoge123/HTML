from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import random
# pip3 install pillow
from PIL import Image ,ImageDraw ,ImageFont
from io import BytesIO #内存管理，将图片放入内存中
from django.contrib  import auth
from app01 import myforms,models
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def login(request):
    if request.is_ajax() :
        back_msg={'user':None ,'msg':None }
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        valid_code=request.POST.get('valid_code')
        print(name,pwd,valid_code)
        #判断用户输入的验证码与session存的验证码是否相同
        if valid_code.upper()==request.session.get('valid_code').upper():
            #用户验证
            user=auth.authenticate(request,username=name,password=pwd)
            if user:
                #登录成功，生成session数据
                auth.login(request,user)
                #更新用户状态
                back_msg['user']=name
                back_msg['msg']='登录成功'
            else:
                back_msg['msg']='用户名密码错误'
        else:
            back_msg['msg']='验证码错误'
        return JsonResponse (back_msg)  #给前端返回一个json格式的字典
    return render(request,'login.html')


def get_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def get_code(request):
    # 图片存在本地
    # img=Image .new('RGB',(300,35),color='pink')  #生成图片 （三原色，尺寸，颜色）
    # with open('code.png','wb') as f:
    #     img.save(f,'png')  #指定图片格式进行保存
    # with open('code.png','rb') as f:
    #     data=f.read()

    # 图片存在内存
    # img = Image.new('RGB', (300, 35), color='pink')
    # 生成一个内存管理对象
    # f=BytesIO ()
    # 将图片放到内存中
    # img.sava(f,'png')
    # 从内存中取出
    # data=f.getvalue()

    img=Image .new('RGB',(300,35),color=get_random_color())
    font=ImageFont.truetype('static/font/kumo.ttf',30)
    draw=ImageDraw .Draw(img)
    valid_code=''
    for i in range(5):
        random_num=str(random.randint(0,9))
        random_upper=chr(random.randint(65,90))
        random_lower=chr(random.randint(97,122))
        random_info=random.choice ([random_lower ,random_num ,random_upper])
        # 传入参数x轴（固定），y轴， 随机字符，图片颜色，字体
        draw.text((i * 40 + 50, 3), random_info, get_random_color(), font=font)
        valid_code+=random_info
    print(valid_code )
    request.session['valid_code']=valid_code
    f=BytesIO() #生成内存管理对象
    img.save(f,'png') #指定图片格式，保存到内存
    data=f.getvalue()  #从内存中取出
    return HttpResponse (data)


def register(request):
    if request.is_ajax() :
        back_msg={'user':None ,'msg':None }
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        re_pwd=request.POST.get('re_pwd')
        email=request.POST.get('email')
        myfile=request.FILES.get('myfile')
        print(request.POST)
    #将用户输入的数据进行校验
        form_obj=myforms.RegForms (request.POST)
        # 表单没有错误
        if form_obj.is_valid() :
            if myfile :
                #avatar = myfile 将文件存入指定的路径avatar
                models.UserInfo.objects.create_user(username= name,password=pwd,email=email,avatar=myfile)
            else:
                models.UserInfo.objects.create_user(username=name, password=pwd, email=email)
            back_msg['user']=name
            back_msg['msg']='注册成功'
        else:
            print(form_obj.errors )
            # 向前端返回错误信息
            back_msg['msg']=form_obj.errors
        return JsonResponse(back_msg)
    form_obj = myforms.RegForms()
    return render(request,'register.html',{'form_obj':form_obj})


def index(request):
    article_list=models.Article.objects.all()
    return render(request,'index.html',{'article_list':article_list})


def home_site(request,username,**kwargs ): #接收一个或多个参数
    # print(kwargs )
    # username=username
    print(username)
    user=models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,'error.html')
    # article_list=user.article_set.all()  #反向查
    article_list=models.Article.objects.filter(user__nid=user.nid) #双下划线查询
     #输入作者返回文章<QuerySet [<Article: Article object>, <Article: Article object>]>
    if kwargs :
        condition=kwargs .get('condition')
        if condition=='tag':
            search_tag=kwargs .get('param')
            # 标签下的所有文章
            article_list=models.Article .objects.filter(user=user) .filter(tag__title=search_tag)
        elif condition=='category':
            search_category=kwargs.get('param')
            article_list=models.Article  .objects.filter(user=user).filter(category__title=search_category)
        elif condition=='archive':
            search_tag=kwargs .get('param')
            # 通过输入时间查询文章
            year,month=search_tag.split('-')
            article_list=models.Article .objects.filter(user=user).filter(create_data__year='year',create_data__month='month')
    print(article_list )


    blog=user.blog
    # 当前站点下每个标签的文章数
    # tag=models.Tag.objects .filter(blog=blog).annotate(c=Count('article__title')).values('title','c')
    # print(tag)
    #当前站点下每个分类的文章数
    category=models.Category .objects.filter(blog=blog).annotate(c=Count('article__title')) .values('title','c')
    print(category)

    # 截断函数，按月截断
    from django.db.models.functions import TruncMonth
    # 当前站点下每个月份的文章数
    # 生成y_m对象后,要按照y_m进行分组 ——》values('y_m')
    mouth_list=models.Article .objects .all().filter(user=user).annotate(y_m=TruncMonth('create_date')).values('y_m')\
        .annotate(c=Count('y_m')).values_list('y_m','c')
    print(mouth_list )
    # for i in a_list:
    #     print(i.y_m)  #循环出时间，按月截，从号开始

    return render(request,'home_site.html')


def article_deatil(request,username,article_id):
    username =username
    article=models.Article .objects .all().filter(pk=article_id).first()
    return render(request,'article_deatil.html',locals())

import json
from django.db.models import F
def diggit(request):
    back_msg = {'status': None, 'msg': None}
    if request.is_ajax() :
        if request.user.is_authenticated():
            article_id=request.POST.get('article_id')
            is_up=json.loads(request.POST.get('is_up')) # 字符串转成布尔类型

            ret=models.ArticleUpDown.objects.filter(article_id=article_id,user=request.user)
            if ret:
                back_msg['status']=False
                back_msg['msg']='已经点过了'
            else:
                models.ArticleUpDown .objects .cerate(user=request.user,article_id=article_id,is_up=is_up)
                if is_up:
                    models.Article .objects .filter(pk=article_id).update(up_num=F('up_num')+1)
                    back_msg['msg']='点赞成功'
                else:
                    models.Article.objects.filter(pk=article_id).update(up_down=F('down_num') + 1)
                    back_msg['msg']='点踩成功'
                back_msg['status']=True
        else:
            back_msg['status']=False
            back_msg['msg']='请先登录'
    return JsonResponse (back_msg)


def comment(request):
    back_msg={'status':None}
    if request.is_ajax():
        if request.user.is_authenticated :
            user=request.user
            article_id=request.POST.get('article_id')
            content=request.POST.get('content')
            parent_id=request.POST.get('parent_id')
            if parent_id :
                parent=models.Comment.objects.filter(pk=parent_id ) .first()
                back_msg['parent_user']=parent.user.username
                back_msg ['parent_comm']=parent.comm
            ret=models.Comment .objects.cerate(user=user,article_id=article_id,comm=content,parent_comment_id=parent_id)
            back_msg['status']=True
            back_msg['user_name']=user.username
            back_msg['create_time']=ret.create_data.strftime('%Y-%m-%d')
            back_msg['content']=content
        else :
            back_msg={'status':False}
    return JsonResponse (back_msg)

@login_required(login_url='/login/')
def back_home(request):
    user=request.user
    article_list=models.Article .objects.filter(user=user)
    return render(request,'back/back_home.html',locals())

from bs4 import BeautifulSoup
@login_required(login_url='/login/')
def add_article(request):
    if request.method =="POST":
        title=request.POST.get('title')
        content=request.POST.get('article')
        soup=BeautifulSoup(content,'html.parser')
        l1=soup.find_all()
        for tag in l1:
            if tag.name=='script':
                tag.decomposr()
        # 文章的显示内容
        desc=soup.text[0:150]+'...'
        ret=models.Article.objects.create(user=request.user,title=title,content=str(soup),desc=desc)
        return redirect('/back_home/')
                
from qqc_bbs import settings
import os
def add_photo(request):
    print(request.FILES )
    if request.method =="POST":
        myfile=request.FILES .get('imgFile')
        path=os.path.join(settings.MEDIA_ROOT,'photo',myfile.name)
        with open(path,'w')as f:
            for line in myfile:
                f.write(line)
    return JsonResponse ({'error':0,'url':'/media/photo/'+ myfile.name})
































































