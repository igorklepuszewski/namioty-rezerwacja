from django import forms
from rezerwacje.models import Namiot

KOLORY_FORM_CHOICES = [("", "-------")] + Namiot.KOLORY_CHOICES
STANDARD_FORM_CHOICES = [("", "-------")] + Namiot.STANDARD_CHOICES

class NamiotForm(forms.ModelForm):
    kolor = forms.ChoiceField(choices=KOLORY_FORM_CHOICES, required=False)
    rozmiar = forms.IntegerField(min_value=1, required=False)
    standard = forms.ChoiceField(choices=STANDARD_FORM_CHOICES, required=False)

    class Meta:
        model = Namiot
        fields = ["kolor", "rozmiar", "standard"]
