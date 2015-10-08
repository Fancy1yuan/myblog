# -*-coding:utf-8-*-
from django.shortcuts import render
from models import Article, Catagory, Tag, UserProfile

# 返回现在所有分类下的文章数目
def get_catagory():
    catagorys = Catagory.objects.all()
    result = []
    for catagory in catagorys:
        article_count = Article.objects.filter(catagory=catagory).count()
        setattr(catagory, "article_count", article_count)
        result.append(catagory)
    return result


def get_all_tags():
    tags = Tag.objects.all()
    return tags


def get_recent_post():
    articles = Article.objects.all().order_by('-publish_time')[:5]
    return articles

def cus_render(request, template, result={}):
    if request.user.is_authenticated():
        user = request.user
    else:
        #display bloghost's info if not login
        user = UserProfile.objects.get(id=2)
        setattr(user, "is_authenticated", False)
    result['user'] = user
    result['side_catagorys'] = get_catagory()
    result['side_tags'] = get_all_tags()
    result['recent_post'] = get_recent_post()
    return render(request, template, result)


