from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm, UsuarioChangeForm
from .models import Usuario
from cursos.models import Curso
from django.contrib.auth.views import LoginView
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/cadastrar.html', {'form': form})

class MyLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        return reverse('home')



def home(request):
    if request.user.tipo_usuario == Usuario.RELATOR:
        cursos = Curso.objects.filter(membros=request.user)
        return render(request, 'cursos/home.html', {'cursos': cursos})
    elif request.user.tipo_usuario == Usuario.AVALIADOR:
        cursos = Curso.objects.filter(avaliadores=request.user)
        return render(request, 'cursos/home.html', {'cursos': cursos})
    else:
        return render(request, 'cursos/home.html')

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UsuarioChangeForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def detalhes_usuario(request, user_id=None):
    if user_id:
        usuario = get_object_or_404(Usuario, pk=user_id)
        if usuario.tipo_usuario == Usuario.AVALIADOR:
            cursos_usuario = Curso.objects.filter(avaliadores=usuario)
        elif usuario.tipo_usuario == Usuario.GERENCIADOR:
            cursos_usuario = Curso.objects.filter(gerenciador=usuario)
        else:
            cursos_usuario = Curso.objects.filter(membros=usuario)

        if request.user.tipo_usuario == Usuario.AVALIADOR:
            cursos_comum = cursos_usuario.filter(avaliadores=request.user)
        elif request.user.tipo_usuario == Usuario.GERENCIADOR:
            cursos_comum = cursos_usuario.filter(gerenciador=request.user)
        else:
            cursos_comum = cursos_usuario.filter(membros=request.user)

        context = {
            'usuario': usuario,
            'cursos': cursos_comum,
        }
    else:
        context = {
            'usuario': request.user,
            'cursos': None,
        }
    return render(request, 'usuarios/detalhes_usuario.html', context)


def listar_relatores(request):
    relatores = Usuario.objects.filter(tipo_usuario=Usuario.RELATOR)
    return render(request, 'cursos/listar_relatores.html', {'relatores': relatores})

