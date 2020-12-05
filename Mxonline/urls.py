from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include

import xadmin
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView,SendSmsView,DynamicLoginView,RegisterView
from apps.organizations.views import OrgView
#取消csrf_token的工具
from django.views.decorators.csrf import csrf_exempt

#关于静态文件图片的访问
from django.views.static import serve

#配置上传文件的路径
from Mxonline.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin /', admin.site.urls),
    path('xadmin/', xadmin.site.urls),


    #下面两行二选一 template_name="index.html" 和 template_name="base.html" 二选一
    path('', TemplateView.as_view(template_name="index1.html"),name='index'),  #TemplateView 后面直接跟路径
    #path('', TemplateView.as_view(template_name="base.html"),name='index'),




    #账号登录的视图
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


    #1、为了整理、上传的图片、我们把所有的上传文件放到media文件夹下面、并且为它创建url访问地址   在setting当中设置两行 151行 152行
    #2、设置了setting之后、依然是一个破图、显示不了
    #3、配置关于media中图片的访问
    #4、r'^media/(?P<path>.*)$' 的意思是取出media文件夹后面的文件把他放到path这个路径当中,
    #5、server 静态文件的访问url 地址， 这个地址是key:value的形式存储在 Media_root路径下面
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),


    # 课程机构
    # url(r'^org_list/',OrgView.as_view(), name = 'org_list'),
    url(r'^org/',include(('apps.organizations.urls',"organizations"),namespace='org')),

    #用户相关操作
    url(r'^op/', include(('apps.operation.urls', "operations"), namespace="op")),

]
