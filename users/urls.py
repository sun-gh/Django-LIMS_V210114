from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


#  定义用户url
app_name = 'users'

urlpatterns = [
    # 登录与注册
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

    # 修改密码
    path('password-change/', auth_views.PasswordChangeView.as_view(
                            template_name="account/password_change_form.html",
                            success_url=reverse_lazy('users:password_change_done')), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
                                template_name="account/password_change_done.html"), name='password_change_done'),

    path('test/', views.test,),
]
