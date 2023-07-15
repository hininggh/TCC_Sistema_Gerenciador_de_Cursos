from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register, edit_user, detalhes_usuario

urlpatterns = [
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('cadastrar/', register, name='register'),
    path('editar_perfil/', edit_user, name='edit_user'),
    path('detalhes_usuario/<int:user_id>/', detalhes_usuario, name='detalhes_usuario'),
    path('detalhes_usuario/', detalhes_usuario, name='detalhes_usuario'),
]