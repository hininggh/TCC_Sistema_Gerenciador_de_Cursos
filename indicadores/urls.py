from django.urls import path
from .views import indicador_detalhes
from .views import enviar_arquivo, apagar_conteudo

urlpatterns = [
    path('enviar_arquivo/<int:indicador_man_id>/', enviar_arquivo, name='enviar_arquivo'),
    path('apagar_conteudo/<int:indicador_man_id>/', apagar_conteudo, name='apagar_conteudo'),
    path('indicador_detalhes/<int:indicador_man_id>/', indicador_detalhes, name='indicador_detalhes'),
]