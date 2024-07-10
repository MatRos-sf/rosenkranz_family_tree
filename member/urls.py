from django.urls import path

from .views import MemberCreateView

urlpatterns = [path("create/", MemberCreateView.as_view(), name="member-create")]
