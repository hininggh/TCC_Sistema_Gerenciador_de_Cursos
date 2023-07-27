from django.db import models
from usuarios.models import Usuario
from validators import validate_pdf_file

class IndicadorInfo(models.Model):
    ORGANIZACAO = 'O'
    CORPO_DOCENTE = 'C'
    INFRAESTRUTURA = 'I'
    DIMENSOES = [
        (ORGANIZACAO, 'Organização Didático-Pedagógica'),
        (CORPO_DOCENTE, 'Corpo Docente e Tutorial'),
        (INFRAESTRUTURA, 'Infraestrutura'),
    ]
    nome = models.CharField(max_length=255)
    dimensao = models.CharField(max_length=1, choices=DIMENSOES)
    mensagem_aviso = models.TextField(blank=True)
    tabela_conceitos = models.JSONField()

class IndicadorMan(models.Model):
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)
    indicador_info = models.ForeignKey('IndicadorInfo', on_delete=models.CASCADE)
    nsa = models.BooleanField(default=False)
    nivel_suposto = models.IntegerField(null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    conteudo = models.FileField(upload_to='relatorios/', blank=True, validators=[validate_pdf_file])
    usuario_relatorio = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='relatorios')
