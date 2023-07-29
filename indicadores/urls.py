from django.urls import path
from . import views
from .views import indicador_detalhes, indicador_detalhes_ava
from .views import enviar_arquivo, apagar_conteudo

app_name = 'indicadores'

urlpatterns = [
    path('enviar_arquivo/<int:pk>/', enviar_arquivo, name='enviar_arquivo'),
    path('apagar_conteudo/<int:indicador_man_id>/', apagar_conteudo, name='apagar_conteudo'),
    path('indicador_detalhes/<int:indicador_man_id>/', indicador_detalhes, name='indicador_detalhes'),
    path('indicador_detalhes_ava/<int:indicador_man_id>/', indicador_detalhes_ava, name='indicador_detalhes_ava'),
    path('indicadorman/<int:pk>/edit/nsa/', views.indicadorman_edit_nsa, name='indicadorman_edit_nsa'),
    path('indicadorman/<int:pk>/edit/nivelsuposto/', views.indicadorman_edit_nivelsuposto, name='indicadorman_edit_nivelsuposto'),
    path('baixar_conteudo/<int:indicador_man_id>/', views.baixar_conteudo, name='baixar_conteudo'),

]