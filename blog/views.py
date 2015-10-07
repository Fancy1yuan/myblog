#-*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from forms import UserProfileForm, ArticleForm
from models import UserProfile, Article, Comment, Tag, Catagory, Message
from django.views.generic.base import View
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

max_article_per_page = 5

def index(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        #display bloghost's info if not login
        user = UserProfile.objects.get(id=2)
        setattr(user, "is_authenticated", False)
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
        'user': user,
        'cur_page': page,
        'articles': articles
    }
    return render(request, 'Index.html', result)

def detail(request):
    return render(request, 'Detail.html')

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
                return render(request, self.template, data)
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
        if request.user.is_authenticated():
            user = request.user
        else:
            user = UserProfile.objects.get(id=2)
        catagorys = Catagory.objects.all()
        tags = Tag.objects.all()
        form = ArticleForm()
        result = {
            'user': user,
            'catagorys': catagorys,
            'tags': tags,
            'form': form
        }
        if user.is_authenticated():
            return render(request, self.template, result)
        else:
            return HttpResponseRedirect('/blog/')

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
        if keyword:
            if request.user.is_authenticated():
                user = request.user
            else:
                user = UserProfile.objects.get(id=2)
            search_article = Article.objects.filter(title__icontains=keyword).order_by('-publish_time')
            articles = Paginator(search_article, max_article_per_page)
            page = int(request.GET.get('page', 1))
            try:
                articles = articles.page(page)
            except PageNotAnInteger:
                articles = articles.page(1)
            except EmptyPage:
                articles = articles.page(articles.num_pages)
            result = {
                'user': user,
                'keyword': keyword,
                'articles': articles,
                'cur_page': page
            }
            return render(request, 'Search_result.html', result)
        else:
            return HttpResponseRedirect('/blog/')

    except Exception as e:
        return HttpResponseRedirect('/blog/')


def about(request):
    return render(request, 'About.html')


class Contact(View):
    template = 'Contact.html'

    def get(self, request):
        return render(request, self.template)

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
        result = {
            'form': self.form
        }
        result.update(csrf(request))
        user = UserProfile.objects.all()
        for us in user[1:4]:
            us.set_password(us.password)
            us.save()

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
                return render(request, self.templates, {'form': self.form})
        except Exception as e:
                pass


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