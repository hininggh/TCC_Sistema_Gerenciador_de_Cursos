from django.db import models
from usuarios.models import Usuario
from validators import validate_pdf_file
import os


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
    membros = models.ManyToManyField(Usuario, related_name='cursos_membros')
    avaliadores = models.ManyToManyField(Usuario, related_name='avaliadores')

