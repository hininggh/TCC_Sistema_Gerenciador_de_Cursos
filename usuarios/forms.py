from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'nome', 'tipo_usuario', 'email', 'telefone')

class UsuarioChangeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome', 'tipo_usuario', 'email', 'telefone')