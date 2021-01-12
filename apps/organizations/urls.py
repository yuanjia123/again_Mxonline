from django.conf.urls import url
from apps.organizations.views import OrgView,AddAskView,OrgHomeView,OrgTeacherView,OrgDescView,OrgCourseView,TeacherListView
from django.urls import include, path

urlpatterns = [
    #机构页面的url
    url(r"^list/$",OrgView.as_view(),name = "list"),
    #咨询Url
    url(r"^add_ask/$",AddAskView.as_view(),name = "add_ask"),
    #组织机构详细页面 路由一
    #url(r'^(?P<org_id>\d+)/$',OrgHomeView.as_view(),name = "home"),
    #组织机构详细页面 路由二
    path('<int:org_id>/',OrgHomeView.as_view(),name = "home"),

    #机构教师列表
    url(r'^(?P<org_id>\d+)/teacher/$',OrgTeacherView.as_view(),name = "teacher"),
    #机构的介绍页
    url(r"^(?P<org_id>\d+)/desc/$",OrgDescView.as_view(),name = "desc"),

    #机构的课程页面
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),

    #讲师列表页面
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
]