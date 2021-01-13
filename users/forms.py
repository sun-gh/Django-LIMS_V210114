from django import forms
# from .models import Person
from captcha.fields import CaptchaField
# from django.contrib.admin.widgets import AdminDateWidget


class RegModForm(forms.Form):

    # 定义注册表单
    username = forms.CharField(label="用户名", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pwd1 = forms.CharField(label="输入密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    pwd2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="真实姓名", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码")
