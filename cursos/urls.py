from django.urls import path
from .views import listar_relatores
from .views import criar_curso, detalhes_curso_gen
from .views import detalhes_curso_gen, atualizar_mural_gen, atualizar_mural_eq

urlpatterns = [
    path('listar_relatores/', listar_relatores, name='listar_relatores'),
    path('criar_curso/', criar_curso, name='criar_curso'),
    path('detalhes_curso_gen/<int:curso_id>/', detalhes_curso_gen, name='detalhes_curso_gen'),
    path('detalhes_curso_gen/<int:curso_id>/', detalhes_curso_gen, name='detalhes_curso_gen'),
    path('atualizar_mural_gen/<int:curso_id>/', atualizar_mural_gen, name='atualizar_mural_gen'),
    path('atualizar_mural_eq/<int:curso_id>/', atualizar_mural_eq, name='atualizar_mural_eq'),
]