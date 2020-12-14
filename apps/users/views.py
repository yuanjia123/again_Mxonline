from django.shortcuts import render
from django.views.generic.base import View

#数据库查询   以及cook的设置，登录完成以后存在login当中
from django.contrib.auth import authenticate,login,logout
#跳转
from django.http import HttpResponseRedirect,JsonResponse
#跳转
from django.urls import reverse

#验证码、和表单
from apps.users.forms import LoginForm,DynamicLoginForm,DynamicLoginPostForm,RegisterPostForm,RegisterGetForm
#生成随机数的
from apps.utils.random_str import generate_random
#发送验证码的工具
from apps.utils.YunPian import send_single_sms

#云片使用的apikey
from Mxonline.settings import yp_apikey,REDIS_HOST,REDIS_PORT
import redis
from apps.users.models import UserProfile


class RegisterView(View):
    '''
    注册
    '''
    def get(self,request,*args,**kwargs):
        register_get_form = RegisterGetForm()
        return render(request,'register.html',{
            "register_get_form":register_get_form
        })

    def post(self,request,*args,**kwargs):
        #form表单实例化的时候、如果是post请求、需要加上request.POST
        register_post_form = RegisterPostForm(request.POST)

        #如果验证成功、则说明手机号是新的、验证码也和redis当中的一样
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]


            print("验证成功以后会打印这句话")

            #手机号是用户名
            user = UserProfile(username = mobile)

            #设置密码  加密的形式
            user.set_password(password)
            #手机号是手机号
            user.mobile = mobile
            #保存
            user.save()
            #记录登录
            login(request,user)

            #跳转到首页
            return HttpResponseRedirect(reverse("index"))
        else:
            #如果验证失败的话  重新分配图片验证码到 register_get_form表单
            register_get_form = RegisterGetForm()
            return render(request,"register.html",{
                "register_get_form":register_get_form,
                #这个里面有错误信息、传递过去显示出来
                "register_post_form":register_post_form
            })




#短信验证码的    登录验证
class DynamicLoginView(View):
    '''
    短信验证码的    登录验证
    '''

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        next = request.GET.get("next","")
        login_form = DynamicLoginForm()
        return render(request,'login.html',{
            'login_form':login_form,
            'next':next
        })


    def post(self,request,*args,**kwargs):
        login_form = DynamicLoginPostForm(request.POST)

        #设置一个变量、登录报错以后、让页面还停留在动态短信登陆页面
        dynamic_login = True

        #如果短信验证码、验证成功
        if login_form.is_valid():
            # 没有账号可以登录  思路：先判断用户是否存在、如果存在 ...如果不存在先注册、给随机密码在登录、看以后代码
            # 2、提取手机号
            mobile = login_form.cleaned_data['mobile']

            #提取手机号
            existed_users = UserProfile.objects.filter(mobile=mobile)
            #如果手机号存在（用户存在）
            if existed_users:
                #把手机号给 login记录一下
                user = existed_users[0]

            #如果手机号不存在 （用户不保存在）
            else:
                #添加用户
                user = UserProfile(username=mobile)
                #添加用户名字
                user.password = user

                #添加随机密码
                # 3、生成随机数验证码、不怕爬虫去伪造
                password = generate_random(10, 2)
                user.set_password(password)
                #保存新用户的手机号
                user.mobile = mobile
                #保存密码
                user.save()
            #保存用户的信息
            login(request, user)

            #获取next
            next = request.GET.get('next', "")
            if next:
                # 直接跳转到http://127.0.0.1:8001/course/1/lesson/  这个页面
                return HttpResponseRedirect(next)

            # 跳转到主页
            return HttpResponseRedirect(reverse("index"))


        else:
            #传递这个图片验证码的、表单是因为：如果短信验证码登录报错、重新实例化 验证码对象、传递到前端登陆页面、就不用刷新登陆页面
            d_form = DynamicLoginForm()


            #如果短信验证码验证失败、会接受DynamicLoginPostForm 类的验证错误
            return render(request, "login.html", {"login_form": login_form,
                                                  "dynamic_login":dynamic_login,
                                                  'd_form':d_form})

#发送验证码
class SendSmsView(View):
    '''
    发送验证码
    '''
    def post(self,request,*args,**kwargs):
        # 实例化验证码表单
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            #当验证通过、1、会自动完成用户的验证码验证

            #2、提取手机号    ajax只是给send_sms地址发送了手机号、和验证码、133行验证了图形验证码并通过、137行提取了手机号、
            mobile = send_sms_form.cleaned_data['mobile']

            #3、随机数验证码
            code = generate_random(4,0)

            #发送短信验证码给137行传过来的手机号
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
        #在公开课、详细章节页面、点击开始学习如果没有登录、会跳转到登陆页面、在get方法中拿到要访问的页面、
        next = request.GET.get("next","")

        #实例化图片验证码表单
        login_form = DynamicLoginForm()

        #否则跳转到登陆页面  并且传递验证码给登录页面
        return render(request,'login.html',{
            "login_form":login_form,
            'next':next
        })

    def post(self,request,*args,**kwargs):
        #实例化表单
        login_form = LoginForm(request.POST)

        #表单验证可以说是 输入框验证、1、验证是否有值、2、验证输入的值是否大于 3
        #表单验证如果验证通过就会进入 账号、密码逻辑
        if login_form.is_valid():
            #取出这个里面的值/清洗以后的值
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            #验证用户名、密码是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 如果登录成功  拿到?next=/course/1/lesson/  其中？后面的数据、登录成功以后直接跳转到课程的详细章节页面
                next = request.GET.get('next', "")

                # 如果登录成功、记录登录信息     调用login以后、就是一种登录的状态
                login(request, user)
                # 跳转到主页   index  就是  主页name属性修改后的属性

                #如果存在next
                if next:
                    #直接跳转到http://127.0.0.1:8001/course/1/lesson/  这个页面
                    return HttpResponseRedirect(next) #如果存在next



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