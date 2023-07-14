from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
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
    email = models.EmailField(blank=False)
    telefone = models.CharField(max_length=20)