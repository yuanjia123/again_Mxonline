from django import forms

class LoginForm(forms.Form):
    #名称要必须和视图中的名字一样
    username = forms.CharField(required=True,min_length=2)  #required=True必填字段
    password = forms.CharField(required=True,min_length=3) #max_length=3  最小三个字段