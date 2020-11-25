from django.shortcuts import render
from django.views.generic.base import View

#把课程相关系的模型拿到
from apps.organizations.models import CourseOrg,City

from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from Mxonline.settings import MEDIA_URL
class OrgaView(View):
    def get(self, request, *args, **kwargs):
        #从数据库中获取 课程机构 全部的数据
        all_orgs = CourseOrg.objects.all()
        #查询多少家机构
        org_nums = CourseOrg.objects.count()

        #查询所有的城市
        all_citys = City.objects.all()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        #对课程机构数据进行分页     per_page=5每页显示5条数据
        p = Paginator(all_orgs,per_page=2, request=request)

        orgs = p.page(page)

        #
        return render(request, 'org_list.html',{
            #传递数据到  课程机构的页面 ,orgs是分页以后的对象
            "all_orgs":orgs,
            #传递上传照片的路径
            # "MEDIA_URL":MEDIA_URL
            "org_nums":org_nums,
            'all_citys':all_citys,
        })
