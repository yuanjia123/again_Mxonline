from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include

import xadmin
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView,SendSmsView,DynamicLoginView,RegisterView
from apps.organizations.views import OrgaView
#取消csrf_token的工具
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

#配置上传文件的路径
from Mxonline.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin /', admin.site.urls),
    path('xadmin/', xadmin.site.urls),


    #下面两行二选一 template_name="index.html" 和 template_name="base.html" 二选一
    path('', TemplateView.as_view(template_name="index1.html"),name='index'),  #TemplateView 后面直接跟路径
    #path('', TemplateView.as_view(template_name="base.html"),name='index'),




    #登录的视图
    path('login/', LoginView.as_view(),name = "login"),  #其别名


    #注册
    path('register/', RegisterView.as_view(),name = "register"),  #其别名

    # 退出登录
    path('logout/', LogoutView.as_view(), name="logout"),  # name其别名


    #图片验证码
    url(r'^captcha/',include('captcha.urls')),

    #   服务器发送4位短信验证码
    url(r'^send_sms/',csrf_exempt(SendSmsView.as_view()),name="send_sms"), #接受验证码的接口

    # 接收到验证码、填写验证码、redis是否匹配、如果匹配点击登录
    path('d_login/', csrf_exempt(DynamicLoginView.as_view()), name="d_login"),


    #配置上传文件   文件访问url           MEDIA_ROOT文件的根目录
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),

    # 课程机构
    url(r'^org_list/',OrgaView.as_view(), name = 'org_list'),


]
