from django.contrib import admin
from django.urls import path
import xadmin
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"),name='index'),
    path('login/', LoginView.as_view(),name = "login"),  #其别名

    path('logout/', LogoutView.as_view(),name = "logout"),  #其别名



]
