from django.shortcuts import render, redirect
from django.contrib import auth
from users.models import Person
from django.contrib.auth.decorators import login_required
from .forms import RegModForm
from datetime import datetime

# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        message = "用户名或密码错误！"

        return render(request, "users/login.html", {'message': message})
    else:
        request.session['is_login'] = True  # session是request自带属性，其中的键值对可任意设置
        request.session['user_name'] = user_obj.first_name
        request.session['nickname'] = user_obj.username
        date_join = user_obj.date_joined.strftime("%m-%d-%Y")   # 此处date_joined为datetime对象
        # print(date_join)
        request.session['date_join'] = date_join

        auth.login(request, user_obj)
        return render(request, 'projects/index.html')


@login_required()   # 如果未登录，也就没有登出一说
def logout(request):

    auth.logout(request)  # 会自动清除session
    return redirect('/user/login/')


def register(request):
    # if request.session.get('is_login', None):
    #    return redirect('/projects/index/')

    if request.method == 'POST':
        reg_form = RegModForm(request.POST)

        if reg_form.is_valid():
            user_name = reg_form.cleaned_data.get('username')
            pwd1 = reg_form.cleaned_data.get('pwd1')
            pwd2 = reg_form.cleaned_data.get('pwd2')
            name = reg_form.cleaned_data.get('name')
        # if user_name.strip() and pwd1 and pwd2:
            if pwd1 != pwd2:
                message = '两次输入的密码不同'
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = Person.objects.filter(username=user_name)  # 此处用filter合适，如用get查不到时会报错**
                if same_name_user:
                    message = '用户名已存在！'
                    return render(request, 'users/register.html', locals())

                Person.objects.create_user(username=user_name, password=pwd1, first_name=name)
                return redirect('/user/login/')
        else:
            message = '请检查填写内容！'
            return render(request, 'users/register.html', locals())

    reg_form = RegModForm()
    return render(request, 'users/register.html', locals())


def test(request):
    return render(request, 'users/test.html')
