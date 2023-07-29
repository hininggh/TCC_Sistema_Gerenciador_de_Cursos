from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'inscricao_curricular', 'descricao', 'informacoes_complementares', 'mural_gen', 'capa')


class CapaForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('capa',)