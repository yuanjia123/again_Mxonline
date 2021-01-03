from django.shortcuts import render
from django.views.generic import View
from apps.operation.forms import UserFavForm,CommentsForm
from apps.operation.models import UserFavorite,CourseComments

#如果判断用户没有登录、则返回数据、是Json类型
from django.http import JsonResponse

from apps.courses.models import Course
from apps.organizations.models import Teacher,CourseOrg


class CommentView(View):
    def post(self,request,*args,**kwargs):
        # 1、判断用户是否登录、如果没有登录
        if not request.user.is_authenticated:
            # 如果没登录 js会直接跳转到登录页面
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })

        comment_form = CommentsForm(request.POST)

        if comment_form.is_valid():

            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']

            #给评论表添加数据
            #添加用户
            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments

            #添加课程
            comment.course = course
            comment.save()
            print("------------------------评论插入成功")
            return JsonResponse({
                'status': 'success',
            })

        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误',
            })


class AddFavView(View):
    def post(self,request,*args,**kwargs):
        '''
        功能：用户收藏、取消收藏
        '''
        #1、判断用户是否登录、如果没有登录
        if not request.user.is_authenticated:
            #如果没登录 js会直接跳转到登录页面
            return JsonResponse({
                'status':'fail',
                'msg':'用户未登录'
            })
        #能走到这里说明已经登录了
        #实例化收藏wtfform的对象
        user_fav_form = UserFavForm(request.POST)

        if user_fav_form.is_valid():

            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']


            #数据查询 判断用户是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user,fav_id = fav_id,fav_type=fav_type)

            # 如果收藏了
            if existed_records:
                #删除收藏
                existed_records.delete()
                #(为了判断用户收藏的类型)  等于1说明收藏的是课程
                if fav_type == 1:
                    #查到是收藏的哪个课程、
                    course = Course.objects.get(id = fav_id)
                    #对课程的收藏数字段进行减一
                    course.fav_nums -= 1
                    course.save()

                elif fav_type == 2:
                    courseorg = CourseOrg.objects.get(id = fav_id)
                    courseorg.fav_nums -= 1
                    courseorg.save()

                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()


                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏'
                })

            #如果用户没有收藏、添加收藏
            else:
                user_fav = UserFavorite()
                #给收藏表 新增fav_id数据
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                #哪个用户收藏的数据
                user_fav.user = request.user
                #保存
                user_fav.save()

                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏',
                })
        #验证失败  回复fail
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误',
            })




