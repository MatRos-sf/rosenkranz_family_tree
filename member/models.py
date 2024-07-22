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
    # CHILD = 6, "Child"
    STEPMOTHER = 7, "Stepmother"
    STEPFATHER = 8, "Stepfather"
    WIFE = 9, "Wife"
    HUSBAND = 10, "Husband"
    BROTHER = 11, "Brother"
    SISTER = 12, "Sister"
    # SIBLING = 13, "Sibling"
    HALF_BROTHER = 14, "Half-bother"
    HALF_SISTER = 15, "Half-sister"
    ADOPTED_SON = 16, "Adopted son"
    ADOPTED_DAUGHTER = (
        17,
        "Adopted daughter",
    )
    PARENT = 18, "Parent"

    @classmethod
    def create_reverse_relation(cls, from_person: Member, to_person: Member) -> Member:
        """
        This method returns the reverse relation type for a given relation.
        """
        reverse_relation_mapping = {
            cls.PARTNER: cls.PARTNER,
            cls.MOTHER: cls.mother_and_father_relation_reverse(from_person, to_person),
            cls.FATHER: cls.mother_and_father_relation_reverse(from_person, to_person),
            cls.DAUGHTER: cls.FATHER
            if from_person.gender == GenderChoice.MALE
            else cls.MOTHER,
            cls.SON: cls.FATHER
            if from_person.gender == GenderChoice.MALE
            else cls.MOTHER,
            cls.STEPMOTHER: cls.mother_and_father_relation_reverse(
                from_person, to_person
            ),
            cls.STEPFATHER: cls.mother_and_father_relation_reverse(
                from_person, to_person
            ),
            cls.WIFE: cls.HUSBAND,
            cls.HUSBAND: cls.WIFE,
            cls.BROTHER: cls.get_reverse_sibling_relation(from_person),
            cls.SISTER: cls.get_reverse_sibling_relation(from_person),
            cls.HALF_BROTHER: cls.HALF_BROTHER
            if from_person.gender == GenderChoice.MALE
            else cls.HALF_SISTER,
            cls.HALF_SISTER: cls.HALF_BROTHER
            if from_person.gender == GenderChoice.MALE
            else cls.HALF_SISTER,
            cls.ADOPTED_SON: cls.PARENT,
            cls.ADOPTED_DAUGHTER: cls.PARENT,
            cls.PARENT: cls.ADOPTED_SON
            if from_person.gender == GenderChoice.MALE
            else cls.ADOPTED_DAUGHTER,
        }
        return reverse_relation_mapping.get(from_person.relation_type)

    @classmethod
    def mother_and_father_relation_reverse(cls, from_person, to_person: Member):
        """
        This method returns the reverse relation type for mother and father.
        """
        if to_person.gender == GenderChoice.FEMALE:
            return cls.DAUGHTER if from_person == cls.MOTHER else cls.STEPMOTHER
        elif to_person.gender == GenderChoice.MALE:
            return cls.SON if from_person == cls.FATHER else cls.STEPFATHER

    @classmethod
    def get_reverse_sibling_relation(cls, from_person: "Member") -> "RelationChoice":
        """
        This method returns the reverse relation type for brother and sister.
        """
        return cls.BROTHER if from_person.gender == GenderChoice.MALE else cls.SISTER


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
