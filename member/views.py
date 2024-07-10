from django.views.generic import CreateView

from .forms import MemberForm
from .models import Member


class MemberCreateView(CreateView):
    """
    A Django CreateView for creating a new Member.
    """

    model = Member
    form_class = MemberForm
    template_name = "member/create.html"
