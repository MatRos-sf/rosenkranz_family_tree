from django.db import models
from django.urls import reverse_lazy


class GenderChoice(models.IntegerChoices):
    FEMALE = 1, "Female"
    MALE = 2, "Male"
    OTHER = 3, "Other"


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    third_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100)
    gender = models.PositiveSmallIntegerField(choices=GenderChoice.choices)

    born = models.DateField(blank=True, null=True)
    died = models.DateField(blank=True, null=True)

    description = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now=True)

    def get_success_url(self):
        return reverse_lazy("member-detail", kwargs={"pk": self.pk})

    def has_father(self):
        return self.relations_from.filter(
            relation_type=Relation.RelationChoice.FATHER
        ).exists()

    def has_mother(self):
        return self.relations_from.filter(
            relation_type=Relation.RelationChoice.MOTHER
        ).exists()

    def has_siblings(self):
        return self.relations_from.filter(
            relation_type__in=[
                Relation.RelationChoice.BROTHER,
                Relation.RelationChoice.SISTER,
            ]
        ).exists()


class Relation(models.Model):
    class RelationChoice(models.IntegerChoices):
        PARTNER = 1, "Partner"
        MOTHER = 2, "Mother"
        FATHER = 3, "Father"
        STEPMOTHER = 4, "Stepmother"
        STEPFATHER = 5, "Stepfather"
        WIFE = 6, "Wife"
        HUSBAND = 7, "Husband"
        BROTHER = 8, "Brother"
        SISTER = 9, "Sister"
        HALF_BROTHER = 10, "Half-bother"
        HALF_SISTER = 11, "Half-sister"
        ADOPTED_SON = 12, "Adopted son"
        ADOPTED_DAUGHTER = 13, "Adopted daughter"

    from_person = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="relations_from"
    )
    to_person = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="relations_to"
    )
    relation_type = models.SmallIntegerField(choices=RelationChoice.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
