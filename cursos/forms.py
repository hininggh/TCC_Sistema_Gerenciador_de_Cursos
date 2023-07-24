from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'inscricao_curricular', 'descricao', 'informacoes_complementares', 'mural_gen')

    relatores = forms.CharField(label='Relatores', widget=forms.TextInput(attrs={'id': 'relatores'}), required=False)