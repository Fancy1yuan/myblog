from django.shortcuts import render, HttpResponse

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