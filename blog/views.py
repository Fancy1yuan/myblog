from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from forms import UserProfileForm
from django.views.generic.base import View

# Create your views here.

def index(request):
    return render(request, 'Index.html')

def detail(request):
    return render(request, 'Detail.html')


def about(request):
    return render(request, 'About.html')


def contact(request):
    return render(request, 'Contact.html')


def not_found(request):
    return render(request, '404.html')


def test(request):
    return render(request, 'base.html')


class Register(View):
    templates = 'register.html'
    form = UserProfileForm()

    def get(self, request):
        return render(request, self.templates, {'form': self.form})

    def post(self, request):
        try:
            user = UserProfileForm(request.POST)
            if user.is_valid():
                user.save()
            else:
                return render(request, self.templates, {'form': self.form})
        except Exception as e:
                pass


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active():
            login(request, user)
            # Redirect to a success page.

        else:
            return HttpResponse('<h3>您已被禁，请联系管理员。</h3>')
    else:
        return HttpResponse('chucuola')


def logout(request):
    logout(request)
    # Redirect to a success page.