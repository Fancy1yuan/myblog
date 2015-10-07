#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True, null=True, verbose_name='头像')
    description = models.CharField("个人简介", default="nothing,", max_length=200)
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    phone_num = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号码')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ['-id']

    def __unicode__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField("标签", max_length=20)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Catagory(models.Model):
    name = models.CharField("分类", max_length=30)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField("标题", max_length=50)
    author = models.ForeignKey(UserProfile, verbose_name="作者")
    content = models.TextField("文章内容")
    img = models.ImageField("文章题图", upload_to='article/%Y/%m', blank=True, null=True, max_length=1024*5)
    tags = models.ManyToManyField(Tag, "标签")
    catagory = models.ForeignKey(Catagory, verbose_name="分类")
    publish_time = models.DateTimeField("发表时间", auto_now_add=True)
    praise_count = models.IntegerField("点赞", default=0)


    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['publish_time']

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    user = models.IntegerField("用户ID", blank=True)  #save the user's id if login, and let the visitor comment
    username = models.CharField("称呼", max_length=30)
    useremail = models.EmailField("邮箱")
    content = models.CharField("评论内容", max_length=200)
    article = models.ForeignKey(Article, verbose_name="文章")
    create_time = models.DateTimeField("评论时间", auto_now_add=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ['create_time']

    def __unicode__(self):
        return self.id


class Message(models.Model):
    name = models.CharField("称呼", max_length=50)
    email = models.EmailField("邮箱")
    message = models.TextField("留言")
    create_time = models.DateTimeField("留言时间", auto_now_add=True)

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.id


