from django.forms import ModelForm
from models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fileds = ['username', 'first_name', 'last_name', 'password',
                  'avatar', 'qq', 'email', 'phone_num']
