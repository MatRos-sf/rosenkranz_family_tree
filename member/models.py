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
    """
    This class represents different types of relationships between members.
    """

    PARTNER = 1, "Partner"
    MOTHER = 2, "Mother"
    FATHER = 3, "Father"
    DAUGHTER = 4, "Daughter"
    SON = 5, "Son"
    WIFE = 9, "Wife"
    HUSBAND = 10, "Husband"
    BROTHER = 11, "Brother"
    SISTER = 12, "Sister"
    STEPMOTHER = 7, "Stepmother"
    STEPFATHER = 8, "Stepfather"
    STEPSON = 9, "Stepson"
    STEPDAUGHTER = 10, "Stepdaughter"
    HALF_BROTHER = 14, "Half-bother"
    HALF_SISTER = 15, "Half-sister"
    SIBLING = 13, "Sibling"
    ADOPTED_SON = 16, "Adopted son"
    ADOPTED_DAUGHTER = (
        17,
        "Adopted daughter",
    )
    PARENT = 18, "Parent"
    # CHILD = 6, "Child"

    @classmethod
    def create_reverse_relation(cls, from_person: Member, to_person: Member) -> Member:
        """
        This method returns the reverse relation type for a given relation.
        """
        reverse_relation_mapping = {
            cls.PARTNER: cls.PARTNER,
            cls.MOTHER: cls.get_reverse_child_relation(from_person),
            cls.FATHER: cls.get_reverse_child_relation(from_person),
            cls.DAUGHTER: ...,
            cls.SON: ...,
            cls.STEPMOTHER: cls.get_reverse_child_relation(from_person),
            cls.STEPFATHER: cls.get_reverse_child_relation(from_person),
            cls.WIFE: cls.HUSBAND,
            cls.HUSBAND: cls.WIFE,
            cls.BROTHER: cls.get_reverse_sibling_relation(from_person),
            cls.SISTER: cls.get_reverse_sibling_relation(from_person),
            cls.HALF_BROTHER: cls.get_reverse_sibling_relation(from_person),
            cls.HALF_SISTER: cls.get_reverse_sibling_relation(from_person),
            cls.SIBLING: cls.get_reverse_sibling_relation(from_person),
            cls.ADOPTED_SON: cls.PARENT,
            cls.ADOPTED_DAUGHTER: cls.PARENT,
            cls.PARENT: cls.get_reverse_child_relation(from_person),
        }
        return reverse_relation_mapping.get(from_person.relation_type)

    @classmethod
    def get_reverse_child_relation(cls, from_person):
        """
        This method returns the reverse relation type from child to parent.
        """
        if from_person.relation_type in [cls.MOTHER, cls.FATHER]:
            return cls.SON if from_person.gender == GenderChoice.MALE else cls.DAUGHTER
        elif from_person.relation_type in [cls.STEPMOTHER, cls.STEPFATHER]:
            return (
                cls.STEPSON
                if from_person.gender == GenderChoice.MALE
                else cls.STEPDAUGHTER
            )
        elif from_person.relation_type == cls.PARENT:
            # when child is adopted
            return (
                cls.ADOPTED_SON
                if from_person.gender == GenderChoice.MALE
                else cls.ADOPTED_DAUGHTER
            )
        else:
            return

    @classmethod
    def get_reverse_sibling_relation(cls, from_person: Member):
        """
        This method returns the reverse relation type for brother and sister.
        """
        if from_person.relation_type in [cls.BROTHER, cls.SISTER]:
            return (
                cls.BROTHER if from_person.gender == GenderChoice.MALE else cls.SISTER
            )

        elif from_person.relation_type in [cls.HALF_BROTHER, cls.HALF_SISTER]:
            return (
                cls.HALF_BROTHER
                if from_person.gender == GenderChoice.MALE
                else cls.HALF_SISTER
            )
        elif from_person.relation_type == cls.SIBLING:
            return cls.SIBLING
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
