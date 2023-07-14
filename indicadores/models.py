from django.db import models

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

