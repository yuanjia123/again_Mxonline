from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)

class BaseModel(models.Model):
    #给每张表创建添加时间字段
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        #这样就不会 创建表
        abstract = True

class UserProfile(AbstractUser):
    '''
    继承django自带的类  1、重写就是此类  2、要在setting中去设置，不然django不知道这是我们用户表
    '''
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    mobile = models.CharField(max_length=11, verbose_name="手机号码") #把手机号唯一约束去掉
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="default.jpg")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
# Create your models here.

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
