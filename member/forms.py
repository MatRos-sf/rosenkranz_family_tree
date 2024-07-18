from django import forms
from django.forms.widgets import DateInput
from django.utils import timezone

from .models import Member, Relation


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
        widgets = {
            "born": DateInput(attrs={"type": "date"}),
            "died": DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        born = cleaned_data.get("born")
        died = cleaned_data.get("died")

        if born and died and died < born:
            raise forms.ValidationError("Death date cannot be earlier than birth date.")

        return cleaned_data

    def clean_born(self):
        born = self.cleaned_data.get("born")
        if born and born > timezone.now().date():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return born

    def clean_died(self):
        died = self.cleaned_data.get("died")
        if died and died > timezone.now().date():
            raise forms.ValidationError("Death date cannot be in the future.")
        return died


class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        from_person = cleaned_data.get("from_person")
        to_person = cleaned_data.get("to_person")

        if from_person == to_person:
            raise forms.ValidationError("From and to persons cannot be the same.")

        return cleaned_data
