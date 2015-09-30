#-*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from forms import UserProfileForm, ArticleForm
from models import UserProfile, Article, Comment, Tag, Catagory
from django.views.generic.base import View
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        user = request.user
    else:
        #display bloghost's info if not login
        user = UserProfile.objects.get(id=2)
        setattr(user, "is_authenticated", False)
    return render(request, 'Index.html', {'user': user})

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
        user = request.user
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
        article = ArticleForm(request.POST, request.FILES)
        if article.is_valid():
            catagorys = request.POST.get('catagory', None)
            tags = request.POST.get('tags', None)
        title = request.POST.get('title', None)


def about(request):
    return render(request, 'About.html')


def contact(request):
    return render(request, 'Contact.html')


def not_found(request):
    return render(request, '404.html')


def test(request):
    return render(request, 'base.html')


class RegisterView(View):
    templates = 'register.html'
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