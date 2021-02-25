from django import forms
# from .models import Person
from captcha.fields import CaptchaField
# from django.contrib.admin.widgets import AdminDateWidget


class RegModForm(forms.Form):

    # 定义注册表单
    username = forms.CharField(label="用户名", max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '字母或与数字组合'}))
    pwd1 = forms.CharField(label="输入密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '至少8个字符'}))
    pwd2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '再次输入上面的密码'}))
    name = forms.CharField(label="真实姓名", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码")
