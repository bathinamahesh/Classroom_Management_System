from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'bio', 'location', 'roll']  # profile_pic
