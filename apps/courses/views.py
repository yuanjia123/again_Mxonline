from django.shortcuts import render
from apps.courses.models import Course,CourseTag,CourseResource
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger
from apps.operation.models import UserFavorite,UserCourse,CourseComments
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseCommentsView(View):
    login_url = '/login/'

    def get(self, request, course_id, *arg, **kwargs):
        # 通过传递过来的id 进行查询、查询到要看的具体的课程
        course = Course.objects.get(id=int(course_id))
        # 点击数+1
        course.click_nums += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 如果没有关联
        if not user_courses:
            # 赋值、谁关联了哪门课
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有的同学
        user_courses = UserCourse.objects.filter(course=course)
        # 拿到该课程所有学生的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 通过所有课程有关同学的id、找到所有的同学   拿到课程对象
        # user_id__in = user_ids  意思是UserCourse表的用户id字段  in [user_ids]     order_by('course__click_nums') 对这些课程进行倒叙排列
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('course__click_nums')[:5]

        # 使用列表生成式、取出不含现在显示的课程  这样写太复杂不推荐这样写
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        related_courses = []
        # 便利所有的课程
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        # 拿到这个课程所对应的课程资源
        comments = CourseComments.objects.filter(course=course)

        #因为评论页面很多信息和 课程页面很多数据都是共享的、所以直接复制课程列表页面
        #拿到这个课程所对应的评论
        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            'course_resources': course_resources,
            'related_courses': related_courses,
            'comments':comments
        })


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


        #用户推荐  一个标签  有这种方式
        #tag = course.tag
        #related_courses = []
        #if tag:
            #查找 相同标签的课程、做热门推荐
            # 比如：flask和django都是python就是相同标签。
            # [:3]：寻找前三个 。
            # exclude(id=course.id)：意思是显示除了当前课程   当标签只有一个的时候、可以这样写
            #related_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]

        #用户推荐：一个文章有多个标签、 拿到课程所对应的所有的标签对象
        tags = course.coursetag_set.all()

        #第一种方式
        # tag_li = []
        # for tag in tags:
        #     tag_li.append(tag.tag)

        # 第二种方式  列表推到是  把所有的标签放到一个列表当中去
        tag_list = [tag.tag for tag in tags]
        # 以上两种写法都是把 当前的课程所对应的标签放到  tag_list当中


        #查找在列表当中的标签   标签tag__in=tag_list  意思是 where tag in ['python','web']
        #当一个课程有多个标签的时候 、要寻找和他相似的课程、用下面的方法  俗称 多对多   exclude(course__id=course.id):除了的意思
        #在标签表查询、所有在list里面的标签、 不包含                          如果要对course课程当中的name字段进行过滤可以使用  course__name
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        #set对象
        related_courses = set()
        #查找相同标签的  课程、放到set类型的related_courses当中
        for course_tag in course_tags:
            #遍历这个标签列表、拿到每个标签的课程、添加到set当中去
            related_courses.add(course_tag.course)


        return render(request,"course-detail.html",{
            "course":course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
            "related_courses": related_courses
        })


class CourseLessonView(LoginRequiredMixin, View):
    '''
    登陆以后、才能访问课程详细章详细页面
    0、在django官方文档当中搜索、login_required
    1、引入类视图的   模块from django.contrib.auth.mixins import LoginRequiredMixin
    2、在login_url中定义、如果未登录、则跳转登录页面
    '''
    login_url = '/login/'
    def get(self, request, course_id, *arg, **kwargs):
        # 通过传递过来的id 进行查询、查询到要看的具体的课程
        course = Course.objects.get(id=int(course_id))
        # 点击数+1
        course.click_nums += 1
        course.save()

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        #如果没有关联
        if not user_courses:
            #赋值、谁关联了哪门课
            user_courses = UserCourse(user=request.user,course=course)
            user_courses.save()

            course.students += 1
            course.save()

        # 学习过该课程的所有的同学
        user_courses = UserCourse.objects.filter(course=course)
        #拿到该课程所有学生的id
        user_ids = [user_course.user.id for user_course in user_courses]
        #通过所有课程有关同学的id、找到所有的同学   拿到课程对象
        #user_id__in = user_ids  意思是UserCourse表的用户id字段  in [user_ids]     order_by('course__click_nums') 对这些课程进行倒叙排列
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('course__click_nums')[:5]


        #使用列表生成式、取出不含现在显示的课程  这样写太复杂不推荐这样写
        #related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        related_courses = []
        # 便利所有的课程
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        #拿到这个课程所对应的课程资源
        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html",{
            "course":course,
            'course_resources':course_resources,
            'related_courses':related_courses
        })


