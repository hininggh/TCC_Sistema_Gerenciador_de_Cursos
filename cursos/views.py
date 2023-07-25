from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Usuario
from .models import Curso
from .forms import CursoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from indicadores.models import IndicadorMan, IndicadorInfo
from .forms import CapaForm


def criar_curso(request, curso_id=None):
    if curso_id:
        curso = get_object_or_404(Curso, pk=curso_id)
    else:
        curso = Curso(gerenciador=request.user)

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            curso = form.save()
            relatores_ids = request.POST.getlist('relatores')
            relatores = Usuario.objects.filter(id__in=relatores_ids)
            curso.membros.set(relatores)
            if not curso_id:
                indicadores_info = IndicadorInfo.objects.all()
                for indicador_info in indicadores_info:
                    IndicadorMan.objects.create(curso=curso, indicador_info=indicador_info)
            return redirect('detalhes_curso_gen', curso_id=curso.id)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/criar_curso.html', {'form': form, 'curso': curso})


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
        return redirect('home')
    else:
        return redirect('criar_curso', curso_id=curso_id)

def buscar_relatores(request):
    q = request.GET.get('q', '')
    relatores = Usuario.objects.filter(tipo_usuario=Usuario.RELATOR)
    if q:
        relatores = relatores.filter(nome__icontains=q)
    data = [{'id': relator.id, 'nome': relator.nome} for relator in relatores]
    return JsonResponse(data, safe=False)


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
    if request.method == 'POST':
        form = CapaForm(request.POST, request.FILES)
        if form.is_valid():
            curso.capa = form.cleaned_data['capa']
            curso.usuario_capa = request.user
            curso.save()
            return redirect('detalhes_curso_gen', curso_id=curso.id)
    else:
        form = CapaForm()
    context = {
        'curso': curso,
        'relatores': relatores,
        'indicadores_por_dimensao': indicadores_por_dimensao,
        'form': form,
    }
    return render(request, 'cursos/detalhes_curso_gen.html', context)


def apagar_capa(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    curso.capa.delete()
    curso.usuario_capa = None
    curso.save()
    return redirect('detalhes_curso', curso_id=curso.id)

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
    return render(request, 'cursos/detalhes_curso_relator.html', context)

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