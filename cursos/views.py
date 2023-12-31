from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Usuario
from .models import Curso
from .forms import CursoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from indicadores.models import IndicadorMan, IndicadorInfo
import logging
from .forms import CapaForm


def criar_curso(request, curso_id=None):
    novo_curso = not bool(curso_id)
    curso = get_object_or_404(Curso, pk=curso_id) if curso_id else Curso(gerenciador=request.user)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            curso = form.save()
            # Remove relatores que foram retirados
            relatores_ids = request.POST.getlist('relatores')
            relatores = Usuario.objects.filter(id__in=relatores_ids)
            curso.membros.set(relatores)
            # Remove avaliadores que foram retirados
            avaliadores_ids = request.POST.getlist('avaliadores')
            avaliadores = Usuario.objects.filter(id__in=avaliadores_ids)
            curso.avaliadores.set(avaliadores)
            if novo_curso:
                # Cria os objetos IndicadorMan para cada IndicadorInfo
                indicadores_info = IndicadorInfo.objects.all()
                for indicador_info in indicadores_info:
                    IndicadorMan.objects.create(curso=curso, indicador_info=indicador_info)
            return redirect('cursos:detalhes_curso_gen', curso_id=curso.id)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/criar_curso.html', {'form': form, 'curso': curso})


def buscar_avaliadores(request):
    q = request.GET.get('q', '')
    avaliadores = Usuario.objects.filter(tipo_usuario=Usuario.AVALIADOR)
    if q:
        avaliadores = avaliadores.filter(nome__icontains=q)
    data = [{'id': avaliador.id, 'nome': avaliador.nome} for avaliador in avaliadores]
    return JsonResponse(data, safe=False)
def buscar_relatores(request):
    q = request.GET.get('q', '')
    relatores = Usuario.objects.filter(tipo_usuario=Usuario.RELATOR)
    if q:
        relatores = relatores.filter(nome__icontains=q)
    data = [{'id': relator.id, 'nome': relator.nome} for relator in relatores]
    return JsonResponse(data, safe=False)


def excluir_curso(request, curso_id):
    if request.method == 'POST':
        curso = get_object_or_404(Curso, pk=curso_id)
        indicadores_man = IndicadorMan.objects.filter(curso=curso)
        for indicador_man in indicadores_man:
            if indicador_man.conteudo:
                indicador_man.conteudo.delete()
            indicador_man.delete()
        if curso.capa:
            curso.capa.delete()
        curso.delete()
        return redirect('usuarios:home')
    else:
        return redirect('cursos:criar_curso', curso_id=curso_id)



@require_POST
def atualizar_mural_gen(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.user != curso.gerenciador:
        return JsonResponse({'error': 'Apenas o gerenciador pode atualizar o mural gen.'}, status=403)
    novo_texto = request.POST.get('novo_texto')
    if novo_texto is not None:
        curso.mural_gen = novo_texto
        curso.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Nenhum texto fornecido.'}, status=400)

@require_POST
def atualizar_mural_eq(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if not curso.membros.filter(pk=request.user.pk).exists():
        return JsonResponse({'error': 'Apenas relatores podem atualizar o mural eq.'}, status=403)
    novo_texto = request.POST.get('novo_texto')
    if novo_texto is not None:
        curso.mural_eq = novo_texto
        curso.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Nenhum texto fornecido.'}, status=400)

def detalhes_curso_gen(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    relatores = curso.membros.filter(tipo_usuario=Usuario.RELATOR)
    indicadores_man = IndicadorMan.objects.filter(curso=curso).select_related('indicador_info')
    indicadores_por_dimensao = {}
    for indicador_man in indicadores_man:
        dimensao = indicador_man.indicador_info.get_dimensao_display()
        if dimensao not in indicadores_por_dimensao:
            indicadores_por_dimensao[dimensao] = []
        indicadores_por_dimensao[dimensao].append(indicador_man)

    context = {
        'curso': curso,
        'relatores': relatores,
        'indicadores_por_dimensao': indicadores_por_dimensao,
    }
    return render(request, 'cursos/detalhes_curso_gen.html', context)


def curso_resumo(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    relatores = curso.membros.filter(tipo_usuario=Usuario.RELATOR)
    indicadores_man = IndicadorMan.objects.filter(curso=curso).select_related('indicador_info')
    indicadores_por_dimensao = {}
    for indicador_man in indicadores_man:
        dimensao = indicador_man.indicador_info.get_dimensao_display()
        if dimensao not in indicadores_por_dimensao:
            indicadores_por_dimensao[dimensao] = []
        indicadores_por_dimensao[dimensao].append(indicador_man)
    context = {
        'curso': curso,
        'relatores': relatores,
        'indicadores_por_dimensao': indicadores_por_dimensao,
    }
    return render(request, 'cursos/curso.html', context)

def detalhes_curso_relator(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    relatores = curso.membros.filter(tipo_usuario=Usuario.RELATOR)
    indicadores_man = IndicadorMan.objects.filter(curso=curso).select_related('indicador_info')
    indicadores_por_dimensao = {}
    for indicador_man in indicadores_man:
        dimensao = indicador_man.indicador_info.get_dimensao_display()
        if dimensao not in indicadores_por_dimensao:
            indicadores_por_dimensao[dimensao] = []
        indicadores_por_dimensao[dimensao].append(indicador_man)
    context = {
        'curso': curso,
        'relatores': relatores,
        'indicadores_por_dimensao': indicadores_por_dimensao,
    }
    return render(request, 'cursos/detalhes_curso_gen.html', context)

def detalhes_curso_ava(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    indicadores_man = IndicadorMan.objects.filter(curso=curso).select_related('indicador_info')
    indicadores_por_dimensao = {}
    for indicador_man in indicadores_man:
        dimensao = indicador_man.indicador_info.get_dimensao_display()
        if dimensao not in indicadores_por_dimensao:
            indicadores_por_dimensao[dimensao] = []
        indicadores_por_dimensao[dimensao].append(indicador_man)
    context = {
        'curso': curso,
        'indicadores_por_dimensao': indicadores_por_dimensao,
    }
    return render(request, 'cursos/detalhes_curso_ava.html', context)

def listar_cursos(request):
    cursos = Curso.objects.filter(gerenciador=request.user)
    return render(request, 'cursos/listar_cursos.html', {'cursos': cursos})

def apagar_capa(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    curso.capa.delete()
    curso.usuario_capa = None
    curso.save()
    return redirect('cursos:detalhes_curso_gen', curso_id=curso.id)