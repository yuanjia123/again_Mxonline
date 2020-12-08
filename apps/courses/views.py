from django.shortcuts import render
from apps.courses.models import Course
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger
from apps.operation.models import UserFavorite


class CourseListView(View):
    def get(self,request,*args,**kwargs):
        #最新添加课程
        all_courses = Course.objects.order_by('-add_time')
        #最热课程显示前3个
        hot_courses = Course.objects.order_by('-click_nums')[:3]

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #对课程机构数据进行分页     per_page=5每页显示5条数据
        p = Paginator(all_courses,per_page=2, request=request)
        courses = p.page(page)


        return render(request,'course-list.html',{
            "all_courses":courses,
            'sort':sort,
            'hot_courses':hot_courses
        })



class CourseDetailView(View):
    def get(self,request,course_id,*arg,**kwargs):
        # 通过传递过来的id 进行查询、查询到要看的具体的课程
        course = Course.objects.get(id=int(course_id))
        #点击数+1
        course.click_nums += 1
        course.save()


        has_fav_course = False
        has_fav_org = False

        #判断是否绑定
        if request.user.is_authenticated:
            #条件查询的第一个参数值的是  用户通过request.user可以知道前端是哪个用户
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type = 1):
                has_fav_course = True

            #course.course_org.id  这个课程返回过来的
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type = 2):
                has_fav_org = True

        return render(request,"course-detail.html",{
            "course":course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })

