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

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.third_name} {self.surname}"

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


class RelationChoice(models.IntegerChoices):
    PARTNER = 1, "Partner"
    MOTHER = 2, "Mother"
    FATHER = 3, "Father"
    DAUGHTER = 4, "Daughter"
    SON = 5, "Son"
    CHILD = 6, "Child"
    STEPMOTHER = 7, "Stepmother"
    STEPFATHER = 8, "Stepfather"
    WIFE = 9, "Wife"
    HUSBAND = 10, "Husband"
    BROTHER = 11, "Brother"
    SISTER = 12, "Sister"
    SIBLING = 13, "Sibling"
    HALF_BROTHER = 14, "Half-bother"
    HALF_SISTER = 15, "Half-sister"
    ADOPTED_SON = 16, "Adopted son"
    ADOPTED_DAUGHTER = 17, "Adopted daughter"


class Relation(models.Model):
    from_person = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="relations_from"
    )
    to_person = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="relations_to"
    )
    relation_type = models.SmallIntegerField(choices=RelationChoice.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
