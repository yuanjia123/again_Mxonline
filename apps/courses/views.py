from django.shortcuts import render
from apps.courses.models import Course
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger
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
