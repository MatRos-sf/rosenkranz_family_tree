from typing import Optional

from django.db import models
from django.urls import reverse_lazy


class GenderChoice(models.IntegerChoices):
    FEMALE = 1, "Female"
    MALE = 2, "Male"


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
        middle_name = f"{self.middle_name} " if self.middle_name else ""
        third_name = f"{self.third_name} " if self.third_name else ""
        surname = f"{self.surname}" if self.surname else ""
        return f"{self.first_name} {middle_name} {third_name} {surname}"

    def has_father(self):
        return self.relations_from.filter(relation_type=RelationChoice.SON).exists()

    def has_mother(self):
        return self.relations_from.filter(relation_type=RelationChoice.MOTHER).exists()

    def has_siblings(self):
        return self.relations_from.filter(
            relation_type__in=[
                RelationChoice.BROTHER,
                RelationChoice.SISTER,
            ]
        ).exists()


class RelationChoice(models.IntegerChoices):
    """
    This class represents different types of relationships between members.
    """

    PARTNER = 1, "Partner"
    MOTHER = 2, "Mother"
    FATHER = 3, "Father"
    DAUGHTER = 4, "Daughter"
    SON = 5, "Son"
    WIFE = 6, "Wife"
    HUSBAND = 7, "Husband"
    BROTHER = 8, "Brother"
    SISTER = 9, "Sister"
    STEPMOTHER = 10, "Stepmother"
    STEPFATHER = 11, "Stepfather"
    STEPSON = 12, "Stepson"
    STEPDAUGHTER = 13, "Stepdaughter"
    HALF_BROTHER = 14, "Half-bother"
    HALF_SISTER = 15, "Half-sister"
    SIBLING = 16, "Sibling"
    ADOPTED_SON = 17, "Adopted son"
    ADOPTED_DAUGHTER = (
        18,
        "Adopted daughter",
    )
    PARENT = 19, "Parent"
    # CHILD = 6, "Child"

    @classmethod
    def get_reverse_relation(cls, relation) -> "RelationChoice":
        """
        This method returns the reverse relation type for a given relation.
        """
        to_person = relation.to_person
        relation = relation.relation_type
        reverse_relation_mapping = {
            cls.PARTNER: cls.PARTNER,
            cls.MOTHER: cls.get_child_relation(to_person, relation),
            cls.FATHER: cls.get_child_relation(to_person, relation),
            cls.DAUGHTER: cls.get_parent_relation(to_person, relation),
            cls.SON: cls.get_parent_relation(to_person, relation),
            cls.STEPMOTHER: cls.get_child_relation(to_person, relation),
            cls.STEPFATHER: cls.get_child_relation(to_person, relation),
            cls.WIFE: cls.HUSBAND,
            cls.HUSBAND: cls.WIFE,
            cls.BROTHER: cls.get_sibling_relation(to_person, relation),
            cls.SISTER: cls.get_sibling_relation(to_person, relation),
            cls.HALF_BROTHER: cls.get_sibling_relation(to_person, relation),
            cls.HALF_SISTER: cls.get_sibling_relation(to_person, relation),
            cls.SIBLING: cls.get_sibling_relation(to_person, relation),
            cls.ADOPTED_SON: cls.PARENT,
            cls.ADOPTED_DAUGHTER: cls.PARENT,
            cls.PARENT: cls.get_child_relation(to_person, relation),
        }
        return reverse_relation_mapping.get(relation)

    @classmethod
    def get_child_relation(cls, to_person, relation) -> Optional["RelationChoice"]:
        """
        Example:
            Tom (from_person) is father (relation_type) of X. So X is son or daughter of Tom.
            Reverse relation type: SON or DAUGHTER
        """
        if relation in [cls.MOTHER, cls.FATHER]:
            return cls.SON if to_person.gender == GenderChoice.MALE else cls.DAUGHTER
        elif relation in [cls.STEPMOTHER, cls.STEPFATHER]:
            return (
                cls.STEPSON
                if to_person.gender == GenderChoice.MALE
                else cls.STEPDAUGHTER
            )
        elif relation == cls.PARENT:
            # when child is adopted
            return (
                cls.ADOPTED_SON
                if to_person.gender == GenderChoice.MALE
                else cls.ADOPTED_DAUGHTER
            )
        else:
            return

    @classmethod
    def get_sibling_relation(cls, to_person, relation) -> Optional["RelationChoice"]:
        """
        Example:
            Tom (from_person) is brother (relation_type) of X. So X is brother or sister of Tom.
            Reverse relation type: BROTHER or SISTER
        """
        if relation in [cls.BROTHER, cls.SISTER]:
            return cls.BROTHER if to_person.gender == GenderChoice.MALE else cls.SISTER

        elif relation in [cls.HALF_BROTHER, cls.HALF_SISTER]:
            return (
                cls.HALF_BROTHER
                if to_person.gender == GenderChoice.MALE
                else cls.HALF_SISTER
            )
        elif relation == cls.SIBLING:
            # when sibling is adopted
            return cls.SIBLING
        else:
            return

    @classmethod
    def get_parent_relation(cls, to_person, relation) -> Optional["RelationChoice"]:
        """
        Example:
            Tom (from_person) is son of X. So X is father or mother of Tom.
            Reverse relation type: FATHER or MOTHER
        """
        if relation in [cls.DAUGHTER, cls.SON]:
            return cls.FATHER if to_person.gender == GenderChoice.MALE else cls.MOTHER
        elif relation in [cls.STEPSON, cls.STEPDAUGHTER]:
            return (
                cls.STEPFATHER
                if to_person.gender == GenderChoice.MALE
                else cls.STEPMOTHER
            )
        else:
            return


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

    def get_success_url(self):
        return reverse_lazy("member-detail", kwargs={"pk": self.from_person.pk})

    def __str__(self):
        return f"{self.from_person} is related to {self.to_person} as {self.get_relation_type_display()}"
