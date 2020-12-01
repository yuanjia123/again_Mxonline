from django.conf.urls import url
from apps.organizations.views import OrgView

urlpatterns = [
    url(r"^list/$",OrgView.as_view(),name = "list")
]