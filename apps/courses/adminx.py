import xadmin

from apps.courses.models import Course, Lesson, Video,CourseResource

class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    # menu_style = "accordion"



class BaseSettings(object):
    #xadmin的主题 、皮肤
    enable_themes = True
    #皮肤
    use_bootswatch = True


#注册课程的模型
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]



class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

#设置网站名
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
#主题以及下拉
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)