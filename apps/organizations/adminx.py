import xadmin

from apps.organizations.models import Teacher,CourseOrg,City

#注册老师的模型, 因为课程需要主讲老师
class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    style_fields = {
        "desc": "ueditor"
    }

class CityAdmin(object):
    #显示字段的名称
    list_display = ['id','name','desc']
    #搜多的字段
    search_fields = ['name','desc']
    #过滤器、xadmin当中的  城市表当中的过滤
    list_filter = ['name','desc','add_time']


xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(City,CityAdmin)
