from django import template
from app01.models import *
from django.db.models import Count
from django.db.models.functions import TruncMonth
register=template.Library()

@register .inclusion_tag('classify.html')
def calssify(username):
    user=UserInfo.objects.filter(username=username) .first()
    blog=user.blog
    tag_count=Tag.objects.filter(blog=blog).annotate(c=Count('article__title')) .values('title','c')
    category_count=Category .objects .filter(blog=blog).annotate(c=Count('article__title')) .value('title','c')
    mouth_list=Article.objects.filter(blog=blog).annotate(m=TruncMonth ('create_date')).values('m')\
        .annotate(c=Count('m')).values_list('m','c')
    return {'tag_count':tag_count,'category_count':category_count,'mouth_list':mouth_list,'blog':blog}
































