#-*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, Group
from datetime import datetime

# Create your models here.


class UserProfileManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        根据用户名和密码创建一个用户
        """
        now = datetime.now()
        if not email:
            raise ValueError(u'Email必须填写')
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, email, password, True, True,
                                 **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("昵称", max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username.', 'invalid')
        ])
    first_name = models.CharField("名字", max_length=30, blank=True)
    last_name = models.CharField("姓氏", max_length=30, blank=True)
    email = models.EmailField("邮箱", blank=True, unique=True)
    phone_num = models.IntegerField("手机", max_length=11)
    avatar = models.ImageField("用户头像", upload_to='uploads/avatar/%Y/%m/', height_field=90, width_field=90, default='uploads/avatar/default.jpg')
    description = models.CharField("个人简介", max_length=100)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ['date_joined',]

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Tag(models.Model):
    name = models.CharField("标签", max_length=20)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ['name']

class Catagory(models.Model):
    name = models.CharField("分类", max_length=30)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['name']


class Comment(models.Model):
    user = models.IntegerField("用户ID", blank=True)  #save the user's id if login, and let the visitor comment
    username = models.CharField("称呼", max_length=30)
    useremail = models.EmailField("邮箱")
    content = models.CharField("评论内容", max_length=200)
    create_time = models.DateTimeField("评论时间", auto_now_add=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ['create_time']


class Article(models.Model):
    title = models.CharField("标题", max_length=50)
    author = models.ForeignKey(UserProfile, verbose_name="作者")
    content = models.TextField("文章内容")
    tags = models.ManyToManyField(Tag, "标签")
    comment = models.ForeignKey(Comment, verbose_name="评论")
    catagory = models.ForeignKey(Catagory, verbose_name="分类")
    publish_time = models.DateTimeField("发表时间", auto_now_add=True)
    praise_count = models.IntegerField("点赞")


    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['publish_time']


