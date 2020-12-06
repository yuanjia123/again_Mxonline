from django.shortcuts import render
from django.views.generic.base import View
#把课程相关系的模型拿到
from apps.organizations.models import CourseOrg,City
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from Mxonline.settings import MEDIA_URL

from apps.organizations.forms import AddAskForm
from django.http import JsonResponse
from apps.operation.models import UserFavorite

class OrgCourseView(View):
    '''
    机构课程
    '''
    def get(self,request,org_id,*args,**kwargs):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=1, request=request)
        courses = p.page(page)

        #判断用户是否收藏
        has_fav = False
        #如果已经登录
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, "org-detail-course.html", {
            "all_courses": courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })

class OrgDescView(View):
    '''
    机构详细页面
    '''
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否收藏
        has_fav = False
        # 如果已经登录
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })





class OrgTeacherView(View):
    '''
    机构老师
    '''
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        current_page = "teacher"

        # 判断用户是否收藏
        has_fav = False
        # 如果已经登录
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        #拿到这个机构所有的 老师
        all_teacher = course_org.teacher_set.all()
        return render(request,"org-detail-teachers.html",{
            "all_teacher":all_teacher,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav": has_fav
        })

class OrgHomeView(View):
    '''
    显示机构的详细页面
    '''
    def get(self, request, org_id, *args, **kwargs):
        #查询
        #course_org = CourseOrg.objects.filter(id=int(org_id))

        # 直接传参到view视图  所以用get
        course_org = CourseOrg.objects.get(id=int(org_id))
        #给机构的点击数字段+1
        course_org.click_nums += 1
        course_org.save()

        current_page = "home"

        #显示这个机构的三个课程
        all_courses = course_org.course_set.all()[:3]
        #显示这个机构的一个老师
        all_teacher = course_org.teacher_set.all()[:1]

        # 判断用户是否收藏
        has_fav = False
        # 如果已经登录
        if request.user.is_authenticated:

            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,"org-detail-homepage.html",{
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            "has_fav": has_fav
        })


class AddAskView(View):
    '''
    处理用户消息视图
    '''

    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            #验证通过以后直接保存在数据库
            userask_form.save(commit=True)
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                'msg':'添加出错'
            })



class OrgView(View):
    '''
    授课机构首页
    '''
    def get(self, request, *args, **kwargs):
        #从数据库中获取 课程机构 全部的数据
        all_orgs = CourseOrg.objects.all()


        #查询所有的城市
        all_citys = City.objects.all()

        # 热门点击排序  倒叙-click_nums     正序 click_nums
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        #对机构进行分类  对应前端的get 传参ct = pxjg、ct = gx  、ct = gr等等
        category =request.GET.get("ct","")
        if category:
            #对上面的机构进行二次查询
            all_orgs = all_orgs.filter(category=category)

        #通过城市进行查找
        #1、先拿到传过来的值
        city_id = request.GET.get("city","")
        if city_id:
            #判断是否是数字类型
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        #分类完成以后在进行统计
        # 查询多少家机构
        org_nums = CourseOrg.objects.count()

        #对机构进行排序
        sort = request.GET.get("sort","")
        if sort == 'students':
            # all_orgs.order_by("students")  是正序   -students倒叙
            all_orgs = all_orgs.order_by("-students")
        if sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")


        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #对课程机构数据进行分页     per_page=5每页显示5条数据
        p = Paginator(all_orgs,per_page=10, request=request)
        orgs = p.page(page)



        #
        return render(request, 'org_list.html',{
            #传递数据到  课程机构的页面 ,orgs是分页以后的对象
            "all_orgs":orgs,
            #传递上传照片的路径
            # "MEDIA_URL":MEDIA_URL
            "org_nums":org_nums,
            'all_citys':all_citys,
            'category':category,
            'city_id':city_id,
            'sort':sort,
            'hot_orgs':hot_orgs,
        })
