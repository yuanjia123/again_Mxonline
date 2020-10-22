from django.contrib import admin
from django.urls import path
import xadmin
from django.views.generic import TemplateView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('login/', TemplateView.as_view(template_name="login.html"),name = "login"),  #其别名

]
