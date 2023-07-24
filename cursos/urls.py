from django.urls import path
from .views import listar_relatores
from .views import criar_curso, detalhes_curso_gen
from .views import detalhes_curso_gen, atualizar_mural_gen, atualizar_mural_eq
from .views import buscar_relatores, criar_curso, excluir_curso

urlpatterns = [
    path('listar_relatores/', listar_relatores, name='listar_relatores'),
    path('buscar_relatores/', buscar_relatores, name='buscar_relatores'),
    path('criar_curso/', criar_curso, name='criar_curso'),
    path('editar_curso/<int:curso_id>/', criar_curso, name='editar_curso'),
    path('excluir_curso/<int:curso_id>/', excluir_curso, name='excluir_curso'),
    path('detalhes_curso_gen/<int:curso_id>/', detalhes_curso_gen, name='detalhes_curso_gen'),
    path('detalhes_curso_gen/<int:curso_id>/', detalhes_curso_gen, name='detalhes_curso_gen'),
    path('atualizar_mural_gen/<int:curso_id>/', atualizar_mural_gen, name='atualizar_mural_gen'),
    path('atualizar_mural_eq/<int:curso_id>/', atualizar_mural_eq, name='atualizar_mural_eq'),
]