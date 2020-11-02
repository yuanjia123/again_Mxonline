from django.shortcuts import render
from django.views.generic.base import View

#数据库查询   以及cook的设置，登录完成以后存在login当中
from django.contrib.auth import authenticate,login,logout
#跳转
from django.http import HttpResponseRedirect,JsonResponse
#跳转
from django.urls import reverse

#验证码、和表单
from apps.users.forms import LoginForm,DynamicLoginForm
#生成随机数的
from apps.utils.random_str import generate_random
#发送验证码的工具
from apps.utils.YunPian import send_single_sms

#云片使用的apikey
from Mxonline.settings import yp_apikey,REDIS_HOST,REDIS_PORT
import redis

class SendSmsView(View):
    def post(self,request,*args,**kwargs):
        # 实例化验证码表单
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            #当验证通过、1、会自动完成用户的验证码验证

            #2、提取手机号
            mobile = send_sms_form.cleaned_data['mobile']

            #3、随机数验证码
            code = generate_random(4,0)
            #发送数据
            re_json = send_single_sms(yp_apikey,code,mobile = mobile)
            #如果是200发送成功
            if re_json['code'] == 0:
                #修改字典的值
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)

                # 设置值
                r.set(str(mobile), code)

                # 持久化  (设置验证码5分钟过期)
                r.expire(str(mobile), 300)

            else:
                #否则变成msg
                re_dict["msg"] = re_json["msg"]



        else:
            for key,value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)
#编写退出接口
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        #退出登录、清空cook
        logout(request)
        #跳转到主页
        return HttpResponseRedirect(reverse("index"))

# Create your views here.
class LoginView(View):
    def get(self,request,*args,**kwargs):
        #在index.html页面里面27行 有判断是否登录 如果登录直接跳转到首页
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        #实例化验证码表单
        login_form = DynamicLoginForm()

        #否则跳转到登陆页面  并且传递验证码给登录页面
        return render(request,'login.html',{
            "login_form":login_form
        })

    def post(self,request,*args,**kwargs):
        #实例化表单
        login_form = LoginForm(request.POST)

        #表单验证可以说是 输入框验证、1、验证是否有值、2、验证输入的值是否大于 3
        #表单验证如果验证通过就会进入 账号、密码逻辑
        if login_form.is_valid():
            #这个里面的值/清洗以后的值
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            #验证用户名、密码是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 如果登录成功、记录登录信息     调用login以后、就是一种登录的状态
                login(request, user)
                # 跳转到主页
                return HttpResponseRedirect(reverse('index'))
            #如果账号或者密码验证错误、则传递msg  和 login_form到这个里面
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误","login_form": login_form})

        #如果验证输入错误 传递错误提示login_form到页面 给login.html页面的 79和82行传递
        else:
            return render(request, "login.html", {"login_form": login_form})
        # user_name = request.POST.get("username","")
        # password = request.POST.get("password","")
        #
        # #1、如果用户名不存在提示下面信息   验证的过程
        # if not user_name:
        #     return render(request,"login.html",{"msg":"请输入用户名"})
        # #2、如果密码不存在
        # if not password:
        #     return render(request,"login.html",{"msg":"请输入密码"})
        #
        # #3、如果密码不存在
        # if len(password):
        #     return render(request, "login.html", {"msg": "密码格式不正确"})

        #****思考如何简化 表单验证、如何更简单的使用表单验证


