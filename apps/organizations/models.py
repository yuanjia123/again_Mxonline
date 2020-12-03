from django.db import models
from apps.users.models import BaseModel

# Create your models here.

class City(BaseModel):
    '''
    城市表
    '''
    name = models.CharField(max_length=20, verbose_name=u"城市名")
    desc = models.CharField(max_length=200, verbose_name=u"描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(BaseModel):
    '''
    机构表
    机构表和课程表有关联关系、每个机构有自己的课程
    '''
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="描述")
    tag = models.CharField(default="全国知名", max_length=10, verbose_name="机构标签")
    category = models.CharField(default="pxjg", verbose_name="机构类别", max_length=4,
                                choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")

    #upload_to="org/%Y/%m"  会把图片存在根目录下面、会在数据库中产生一个image字段、存储图片的路径
    #在Mxonline的文件架下面会产生一个org的文件夹、这里存放img
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    def courses(self):
        '''
        通过这个方法， 可以直接找到当前的机构、有哪些课程
        :return:
        '''


        #方式一
        #拿到课程表、  避免环形调用
        #from apps.courses.models import Course
        #拿到当前机构所对应的课程      self是当前类的实例
        #courses = Course.objects.filter(course_org=self)
        #return courses

        #方式二 通过model反向取外键关联数据


        '''
        如果当前的model（机构）是另外一个表(课程)的外键 通过关联表的表名小写_set.all()就能拿到当前机构的课程数据
        '''
        #查询当前机构所有的课程
        # courses = self.course_set.all()

        # 查询当前机构所有的经典课程、只显示前3个
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

from apps.users.models import UserProfile
class Teacher(BaseModel):
    '''
    教师表
    '''
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="用户")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


    #老师的课程数   **老师表关联课程表 在teacher表中使用course_set找到这个老师的所有的课程数
    def course_nums(self):
        return self.course_set.all().count()