from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Usuario
from .models import Curso
from .forms import CursoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from indicadores.models import IndicadorMan, IndicadorInfo
def listar_relatores(request):
    relatores = Usuario.objects.filter(tipo_usuario=Usuario.RELATOR)
    return render(request, 'cursos/listar_relatores.html', {'relatores': relatores})


def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.gerenciador = request.user
            curso.save()
            relatores_ids = form.cleaned_data['relatores'].split(',')
            relatores = Usuario.objects.filter(id__in=relatores_ids)
            curso.membros.set(relatores)
            indicadores_info = IndicadorInfo.objects.all()
            for indicador_info in indicadores_info:
                IndicadorMan.objects.create(curso=curso, indicador_info=indicador_info)
            return redirect('detalhes_curso_gen', curso_id=curso.id)
    else:
        form = CursoForm()
    return render(request, 'cursos/criar_curso.html', {'form': form})

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