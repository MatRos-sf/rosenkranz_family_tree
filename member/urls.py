from django.urls import path

from .views import MemberCreateView, MemberDetailView, RelationCreateView

urlpatterns = [
    path("create/", MemberCreateView.as_view(), name="member-create"),
    path("<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path(
        "<int:pk>/relation/create/",
        RelationCreateView.as_view(),
        name="relation-create",
    ),
]
