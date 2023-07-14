from django.db import models
from usuarios.models import Usuario
from django.core.exceptions import ValidationError
import os

def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('Este campo aceita apenas arquivos PDF.')

class Curso(models.Model):
    nome = models.CharField(max_length=255)
    inscricao_curricular = models.CharField(max_length=255)
    data_criacao = models.DateField()
    descricao = models.TextField()
    gerenciador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    informacoes_complementares = models.TextField(blank=True)
    mural_gen = models.TextField(blank=True)
    mural_eq = models.TextField(blank=True)
    capa = models.FileField(upload_to='capas/', blank=True, validators=[validate_pdf_file])
    usuario_capa = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='cursos_capa')



class Equipe(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    membros = models.ManyToManyField(Usuario)


class Relatorio(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    indicador = models.ForeignKey('indicadores.IndicadorMan', on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)
    conteudo = models.FileField(upload_to='relatorios/', validators=[validate_pdf_file])
    usuario_relatorio = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='relatorios')