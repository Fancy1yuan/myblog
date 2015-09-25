from django.contrib import admin
from blog.models import Tag, Comment, Catagory, Article

# Register your models here.



admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Catagory)
admin.site.register(Article)