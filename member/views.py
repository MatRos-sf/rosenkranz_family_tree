from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import MemberForm, RelationForm
from .models import Member, Relation, RelationChoice


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


class RelationCreateView(CreateView):
    """
    A Django CreateView for creating a new Relation.
    """

    model = Relation
    form_class = RelationForm
    template_name = "member/create.html"
    success_url = reverse_lazy("member-detail")

    def form_valid(self, form):
        instance = form.save()
        # reverse_relation
        Relation.objects.create(
            from_person=instance.to_person,
            to_person=instance.from_person,
            relation_type=RelationChoice.get_reverse_relation(instance),
            created_at=instance.created_at,
        )
        return super().form_valid(form)
