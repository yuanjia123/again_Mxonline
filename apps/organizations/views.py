from django.shortcuts import render
from django.views.generic.base import View

#把课程相关系的模型拿到
from apps.organizations.models import CourseOrg,City

from Mxonline.settings import MEDIA_URL
class OrgaView(View):
    def get(self, request, *args, **kwargs):
        #从数据库中获取 课程机构 全部的数据
        all_orgs = CourseOrg.objects.all()
        #查询多少家机构
        org_nums = CourseOrg.objects.count()

        #查询所有的城市
        all_citys = City.objects.all()
        return render(request, 'org_list.html',{
            #传递数据到  课程机构的页面
            "all_orgs":all_orgs,
            #传递上传照片的路径
            # "MEDIA_URL":MEDIA_URL
            "org_nums":org_nums,
            'all_citys':all_citys,
        })
