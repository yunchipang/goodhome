from django import forms
from .models import User

# class SignUpForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)
#     email = forms.EmailField()
#     name = forms.CharField(max_length=100)  # 添加姓名字段
#     phone = forms.CharField(max_length=15)   # 添加电话字段
#     address = forms.CharField(max_length=255)  # 添加地址字段

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'mailing_address']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
