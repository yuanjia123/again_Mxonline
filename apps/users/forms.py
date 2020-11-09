from django import forms
from captcha.fields import CaptchaField
import redis

from Mxonline.settings import REDIS_HOST, REDIS_PORT

class LoginForm(forms.Form):
    '''

    账号登录的验证
    '''
    #名称要必须和视图中的名字一样
    username = forms.CharField(required=True,min_length=2)  #required=True必填字段
    password = forms.CharField(required=True,min_length=3) #max_length=3  最小三个字段


class DynamicLoginForm(forms.Form):
    '''
    图片验证码的验证
    '''
    captcha = CaptchaField()
    # 手机号
    mobile = forms.CharField(required=True,min_length=11,max_length=11)

class DynamicLoginPostForm(forms.Form):

    '''
    手机动态验证码的验证
    '''
    # 手机号
    mobile = forms.CharField(required=True,min_length=11,max_length=11)
    #发送的动态验证码
    code = forms.CharField(required=True,min_length=4,max_length=4)

    def clean_code(self):
        '''
        验证哪一个字段错误。
        在forms当中做短信验证码    验证操作操作
        :return:
        '''
        #data.get 先获取手机号
        mobile = self.data.get("mobile")
        #在获取验证码
        code = self.data.get("code")
        #连接redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        #获取手机号key  所对应的redis
        redis_code = r.get(str(mobile))
        if code != redis_code:
            #如果发送的code  和 redis里面的code不相等、抛出异常
            raise forms.ValidationError("验证码不正确")

        #直接返回self.cleaned_data
        return self.cleaned_data

        # def code(self):
        #     '''
        #     验证全部(mobile  和  code)字段字段错误。
        #     在forms当中做短信验证码    验证操作操作
        #     :return:
        #     '''
        #     # 先获取手机号
        #     mobile = self.cleaned_data("mobile")
        #     # 在获取验证码
        #     code = self.cleaned_data("code")
        #     # 连接redis
        #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        #     # 获取手机号key  所对应的redis
        #     redis_code = r.get(str(mobile))
        #     if code != redis_code:
        #         # 如果发送的code  和 redis里面的code不相等、抛出异常
        #         raise forms.ValidationError("验证码不正确")
        #
        #     # 直接返回self.cleaned_data
        #     return self.cleaned_data