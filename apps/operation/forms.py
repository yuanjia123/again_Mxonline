import re
from django import forms
from apps.operation.models import UserFavorite,CourseComments

class UserFavForm(forms.ModelForm):
    '''
    收藏的form
    '''
    class Meta:
        model = UserFavorite
        fields = ['fav_id','fav_type']

class CommentsForm(forms.ModelForm):
    '''
    评论的form  使用模型表单
    '''
    class Meta:
        model = CourseComments
        #使用下面这个两个属性
        fields = ['course', 'comments']