from django.urls import path
from . import views
from .views import detalhes_curso_gen, atualizar_mural_gen, atualizar_mural_eq, detalhes_curso_relator, buscar_avaliadores
from .views import buscar_relatores, criar_curso, excluir_curso
from .views import listar_cursos, apagar_capa

app_name = 'cursos'

urlpatterns = [
    path('buscar_relatores/', buscar_relatores, name='buscar_relatores'),
    path('cursos/buscar_avaliadores/', views.buscar_avaliadores, name='buscar_avaliadores'),
    path('criar_curso/', views.criar_curso, name='criar_curso'),
    path('editar_curso/<int:curso_id>/', views.criar_curso, name='editar_curso'),
    path('excluir_curso/<int:curso_id>/', excluir_curso, name='excluir_curso'),
    path('detalhes_curso_gen/<int:curso_id>/', detalhes_curso_gen, name='detalhes_curso_gen'),
    path('detalhes_curso_relator/<int:curso_id>/', detalhes_curso_relator, name='detalhes_curso_relator'),
    path('atualizar_mural_gen/<int:curso_id>/', atualizar_mural_gen, name='atualizar_mural_gen'),
    path('atualizar_mural_eq/<int:curso_id>/', atualizar_mural_eq, name='atualizar_mural_eq'),
    path('listar_cursos/', listar_cursos, name='listar_cursos'),
    path('apagar_capa/<int:curso_id>/', views.apagar_capa, name='apagar_capa'),
    path('cursos/<int:curso_id>/resumo/', views.curso_resumo, name='curso_resumo'),
    path('detalhes_curso_ava/<int:curso_id>/', views.detalhes_curso_ava, name='detalhes_curso_ava'),
]