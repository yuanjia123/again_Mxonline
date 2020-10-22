from django.shortcuts import render
from django.views.generic.base import View

#数据库查询   以及cook的设置，登录完成以后存在login当中
from django.contrib.auth import authenticate,login
#跳转
from django.http import HttpResponseRedirect
#跳转
from django.urls import reverse

# Create your views here.
class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'login.html')

    def post(self,request,*args,**kwargs):
        user_name = request.POST.get("username","")
        password = request.POST.get("password","")
        #验证用户名、密码是否存在
        user = authenticate(username = user_name,password=password)
        if user is not None:
            # 如果登录成功、记录登录信息
            login(request,user)
            #跳转到主页
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,"login.html",{"msg":"用户名或者密码错误"})