from django.urls import path

from .views import MemberCreateView, MemberDetailView

urlpatterns = [
    path("create/", MemberCreateView.as_view(), name="member-create"),
    path("<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
]
