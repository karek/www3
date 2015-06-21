from django import forms
from .models import Gmina, Obwod


class GminaForm(forms.Form):
    gmina = forms.ModelChoiceField(queryset=Gmina.objects.all())


class ObwodForm(forms.ModelForm):
    class Meta:
        model = Obwod
        fields = ['uprawnionych', 'ileKart']