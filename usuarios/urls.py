app_name = 'usuarios'

from django.urls import path
from .views import register, editar_perfil, detalhes_usuario
from .views import listar_relatores
from .views import MyLoginView
from django.contrib.auth.views import LogoutView
from usuarios import views as usuarios_views

urlpatterns = [
    path('', usuarios_views.login_view, name='login'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('home/', usuarios_views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),
    path('cadastrar/', register, name='register'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('detalhes_usuario/<int:user_id>/', detalhes_usuario, name='detalhes_usuario'),
    path('detalhes_usuario/', detalhes_usuario, name='detalhes_usuario'),
    path('listar_relatores/', listar_relatores, name='listar_relatores'),
]