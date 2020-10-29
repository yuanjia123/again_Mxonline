from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    #名称要必须和视图中的名字一样
    username = forms.CharField(required=True,min_length=2)  #required=True必填字段
    password = forms.CharField(required=True,min_length=3) #max_length=3  最小三个字段


class DynamicLoginForm(forms.Form):
    captcha = CaptchaField()
    # 手机号
    mobile = forms.CharField(required=True,min_length=11,max_length=11)
