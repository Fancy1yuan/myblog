#-*- coding:utf-8 -*-
from django.forms import ModelForm
from django import forms
from models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'password',
                  'avatar', 'qq', 'email', 'phone_num']

        widgets = {
            'password': forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码", "min_length": 8, "max_length": 50}),
        }

        error_messages = {
            "password": {
                        "required": "账号密码不能为空",
                        "min_length": "请输入至少8位密码",
                        "max_length": "密码不能超过50位"
            }
        }

