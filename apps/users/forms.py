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
        在forms当中做验证操作
        :return:
        '''
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data