from django.db import models

class Usuario(models.Model):
    GERENCIADOR = 'G'
    RELATOR = 'R'
    AVALIADOR = 'A'
    TIPOS_USUARIO = [
        (GERENCIADOR, 'Gerenciador'),
        (RELATOR, 'Relator'),
        (AVALIADOR, 'Avaliador'),
    ]
    nome = models.CharField(max_length=255)
    tipo_usuario = models.CharField(max_length=1, choices=TIPOS_USUARIO)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)