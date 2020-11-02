from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

import xadmin
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView,SendSmsView,DynamicLoginView

#取消csrf_token的工具
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"),name='index'),
    path('login/', LoginView.as_view(),name = "login"),  #其别名
    path('d_login/', csrf_exempt(DynamicLoginView.as_view()),name = "d_login"),  #其别名

    path('logout/', LogoutView.as_view(),name = "logout"),  #其别名
    url(r'^captcha/',include('captcha.urls')), #图片验证码
    url(r'^send_sms/',csrf_exempt(SendSmsView.as_view()),name="send_sms"), #接受验证码的 接口

]
