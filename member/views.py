from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import MemberForm
from .models import Member


class MemberCreateView(CreateView):
    """
    A Django CreateView for creating a new Member.
    """

    model = Member
    form_class = MemberForm
    template_name = "member/create.html"
    success_url = reverse_lazy("member-detail")


class MemberDetailView(DetailView):
    model = Member
    template_name = "member/detail.html"
