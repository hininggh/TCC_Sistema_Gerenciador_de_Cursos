from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register, edit_user, detalhes_usuario
from .views import listar_relatores
from .views import MyLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('cadastrar/', register, name='register'),
    path('editar_perfil/', edit_user, name='edit_user'),
    path('detalhes_usuario/<int:user_id>/', detalhes_usuario, name='detalhes_usuario'),
    path('detalhes_usuario/', detalhes_usuario, name='detalhes_usuario'),
    path('listar_relatores/', listar_relatores, name='listar_relatores'),
]