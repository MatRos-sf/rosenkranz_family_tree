from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import MemberForm, RelationForm
from .models import Member, Relation


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


# def get_reverse_relation_type(from_person: Member, to_person: Member, relation_type: int) -> int:
#     reverse_relation_mapping = {
#         Relation.RelationChoice.PARTNER: Relation.RelationChoice.PARTNER,
#         Relation.RelationChoice.MOTHER: Relation.if to_person.gender == GenderChoice.FEMALE else Relation.RelationChoice.MOTHER,
#         Relation.RelationChoice.FATHER: Relation.RelationChoice.MOTHER,
#         Relation.RelationChoice.STEPMOTHER: Relation.RelationChoice.STEPFATHER,
#         Relation.RelationChoice.STEPFATHER: Relation.RelationChoice.STEPMOTHER,
#         Relation.RelationChoice.WIFE: Relation.RelationChoice.HUSBAND,


class RelationCreateView(CreateView):
    """
    A Django CreateView for creating a new Relation.
    """

    model = Relation
    form_class = RelationForm
    template_name = "member/create.html"
    success_url = reverse_lazy("member-detail")

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     from_person = form.instance.from_person
    #     to_person = form.instance.to_person
    #     relation_type = form.cleaned_data["relation_type"]
