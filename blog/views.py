#-*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from forms import UserProfileForm, ArticleForm
from models import UserProfile, Article, Comment, Tag, Catagory, Message
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from utils import cus_render

# Create your views here.

max_article_per_page = 5

def index(request):
    articles = Article.objects.all().order_by('-publish_time')
    articles = Paginator(articles, max_article_per_page)
    page = int(request.GET.get('page', 1))
    try:
        articles = articles.page(page)
    except PageNotAnInteger:
        articles = articles.page(1)
    except EmptyPage:
        articles = articles.page(articles.num_pages)
    result = {
        'cur_page': page,
        'articles': articles,
    }
    return cus_render(request, 'Index.html', result)


# # 返回现在所有分类下的文章数目
# def get_catagory():
#     catagorys = Catagory.objects.all()
#     result = []
#     for catagory in catagorys:
#         article_count = Article.objects.filter(catagory=catagory).count()
#         setattr(catagory, "article_count", article_count)
#         result.append(catagory)
#     return result
#
#
# def get_all_tags():
#     tags = Tag.objects.all()
#     return tags
#
#
# def get_recent_post():
#     articles = Article.objects.all().order_by('-publish_time')[:5]
#     return articles


class ArticleView(View):
    template = 'Detail.html'

    def get(self, request):
        try:
            article_id = int(request.GET.get(u'id', 1))
            article = Article.objects.filter(id=article_id)
            if article[0]:
                next_post = Article.objects.filter(id=article_id+1)
                if next_post:
                    next_post = next_post[0]
                previous_post = Article.objects.filter(id=article_id-1)
                if previous_post:
                    previous_post = previous_post[0]
                data = {
                    'article': article[0],
                    'next_post': next_post,
                    'previous_post': previous_post,
                }
                return cus_render(request, self.template, data)
            else:
                return render(request, '404.html')
        except Exception as e:
            return HttpResponseRedirect('/blog/')

    def post(self, request):
        article_id = request.GET.get('id', '')
        if not article_id:
            return HttpResponseRedirect('/blog/article/')
        article_id = int(article_id)
        article = Article.objects.get(id=article_id)
        # handle loged user's comment
        if request.user.is_authenticated():
            user = request.user
            comment = Comment.objects.create(user=user.id, username=user.username, useremail=user.email,
                                             content=request.POST['content'], article=article)
            comment.save()
        else:
            username = request.POST['username']
            email = request.POST['email']
            content = request.POST['content']
            comment = Comment.objects.create(username=username, useremail=email,
                                             content=content, artcile=article)
            comment.save()
        # return current article
        return HttpResponseRedirect('/blog/article/?id=%s' % article_id)


class ArticlePublish(View):
    template = 'ArticlePublish.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/blog/')
        catagorys = Catagory.objects.all()
        tags = Tag.objects.all()
        form = ArticleForm()
        result = {
            'catagorys': catagorys,
            'tags': tags,
            'form': form,
        }
        return cus_render(request, self.template, result)


    def post(self, request):
        try:
            article = ArticleForm(request.POST, request.FILES)
            if article.is_valid():
                article = Article.objects.create(title=request.POST['title'], img=request.FILES['img'] if request.FILES else None, author=request.user,
                                                 content=request.POST['content'], catagory_id=int(request.POST['catagory']))
                article.save()
                tags = request.POST.getlist('tags')
                for tag in tags:
                    tag = Tag.objects.get(id=int(tag))
                    article.tags.add(tag)
                article.save()
            return HttpResponseRedirect('/blog/')
        except Exception as e:
            pass


def search(request):
    try:
        keyword = request.GET.get('keyword', None)
        catagory = request.GET.get('catagory', None)
        tag = request.GET.get('tag', None)
        if keyword:
            search_article = Article.objects.filter(title__icontains=keyword).order_by('-publish_time')
        elif catagory:
            catagory = Catagory.objects.get(name=catagory)
            search_article = Article.objects.filter(catagory=catagory).order_by('-publish_time')
        elif tag:
            tag = Tag.objects.get(name=tag)
            search_article = Article.objects.filter(tags=tag)
        else:
            return HttpResponseRedirect('/blog/')
        page = int(request.GET.get('page', 1))
        articles = Paginator(search_article, max_article_per_page)
        try:
            articles = articles.page(page)
        except PageNotAnInteger:
            articles = articles.page(1)
        except EmptyPage:
            articles = articles.page(articles.num_pages)
        result = {
            'keyword': keyword,
            'catagory': catagory,
            'tag': tag,
            'articles': articles,
            'cur_page': page,
        }
        return cus_render(request, 'Search_result.html', result)

    except Exception as e:
        return HttpResponseRedirect('/blog/')


def about(request):
    return cus_render(request, 'About.html')


class Contact(View):
    template = 'Contact.html'

    def get(self, request):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = UserProfile.objects.get(id=2)
        result = {
            'user': user,
        }
        return cus_render(request, self.template, result)

    def post(self, request):
        message_content = request.POST['message']
        message = Message.objects.create(name=request.POST['name'], email=request.POST['email'],
                                         message=message_content)
        message.save()
        return HttpResponseRedirect('/blog/')


def not_found(request):
    return render(request, '404.html')


class Test(View):

    def get(self, request):
        return render(request, 'test.html')

    def post(self, request):
        pass


class RegisterView(View):
    templates = 'Register.html'
    form = UserProfileForm()

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/blog/')
        result = {
            'form': self.form,
        }

        return render(request, self.templates, result)

    def post(self, request):
        try:
            user = UserProfileForm(request.POST)
            if user.is_valid():
                user = UserProfile.objects.create(username=request.POST[u'username'], password=make_password(request.POST[u'password']),
                                                  first_name=request.POST[u'first_name'], last_name=request.POST[u'last_name'],
                                                  email=request.POST[u'email'], phone_num=request.POST[u'phone_num'] if request.POST[u'phone_num'] else None,
                                                  qq=request.POST[u'qq'])
                user.save()

                return render(request, 'Register_success.html', {})
            else:
                return HttpResponseRedirect('/blog/register/')
        except Exception as e:
                return HttpResponseRedirect('/blog/register/')


@csrf_exempt    # 没做出登陆弹窗，没法加{% csrf_token %},暂时舍弃该功能
def cus_login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # return to success page
                return HttpResponseRedirect('/blog/')

            else:
                return HttpResponse('<h3>您已被禁，请联系管理员。</h3>')
        else:
            return HttpResponse('chucuola')
    except Exception as e:
        return HttpResponseRedirect('/blog/')


def cus_logout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/blog/')

def page_not_found(request):
    return render(request, '404.html')