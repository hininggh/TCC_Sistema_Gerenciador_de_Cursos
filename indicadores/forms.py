from django import forms
from .models import IndicadorMan

class NSAForm(forms.ModelForm):
    class Meta:
        model = IndicadorMan
        fields = ('nsa',)

class NivelSupostoForm(forms.ModelForm):
    class Meta:
        model = IndicadorMan
        fields = ('nivel_suposto',)

class RelatorioForm(forms.Form):
    relatorio = forms.FileField(required=False)

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = IndicadorMan
        fields = ('conteudo',)