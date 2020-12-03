from django import forms
from apps.operation.models import UserAsk
import re

class AddAskForm(forms.ModelForm):
    '''
    表单验证：  表单可以直接继承数据表、  比如这个课程机构页面的用户咨询模块、就继承了用户操作app下面的UserAsk的表
    '''

    #对单独一个字段进行数据判断
    mobile = forms.CharField(max_length=11,min_length=11,required=True)
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
