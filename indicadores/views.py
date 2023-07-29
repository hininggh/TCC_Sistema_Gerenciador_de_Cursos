from django.shortcuts import render, get_object_or_404, redirect
from .forms import NSAForm, NivelSupostoForm, ConteudoForm
from .models import IndicadorMan, IndicadorInfo
from PyPDF2 import PdfMerger  # Importe a classe PdfMerger correta
from usuarios.models import Usuario
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from cursos.models import Curso
from django.utils import timezone
from django.http import FileResponse
from .forms import IndicadorManNSAForm, IndicadorManNivelSupostoForm
from .forms import IndicadorManConteudoForm



def indicador_detalhes(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    curso = indicador_man.curso
    nsa_form = NSAForm(request.POST or None, instance=indicador_man)
    nivel_suposto_form = NivelSupostoForm(request.POST or None, instance=indicador_man)
    if request.method == 'POST':
        if nsa_form.is_valid():
            nsa_form.save()
        if nivel_suposto_form.is_valid():
            nivel_suposto_form.save()
        return redirect('indicadores:indicador_detalhes', indicador_man_id=indicador_man.id)
    # Buscar manualmente o objeto IndicadorInfo relacionado
    indicador_info = IndicadorInfo.objects.get(pk=indicador_man.indicador_info_id)

    context = {
        'nsa_form': nsa_form,
        'nivel_suposto_form': nivel_suposto_form,
        'indicador_man': indicador_man,
        'curso': curso,
        'nome_indicador': indicador_info.nome,
        'mensagem_aviso': indicador_info.mensagem_aviso,
        'tabela_conceitos': indicador_info.tabela_conceitos,
    }
    return render(request, 'indicadores/indicador_detalhes.html', context)

def indicador_detalhes_ava(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    # Buscar manualmente o objeto IndicadorInfo relacionado
    indicador_info = IndicadorInfo.objects.get(pk=indicador_man.indicador_info_id)
    context = {
        'indicador_man': indicador_man,
        'nome_indicador': indicador_info.nome,
        'mensagem_aviso': indicador_info.mensagem_aviso,
        'tabela_conceitos': indicador_info.tabela_conceitos,
    }
    return render(request, 'indicadores/indicador_detalhes_ava.html', context)

#
def indicadorman_edit_nsa(request, pk):
    indicadorman = get_object_or_404(IndicadorMan, pk=pk)
    if request.method == 'POST':
        form = IndicadorManNSAForm(request.POST, instance=indicadorman)
        if form.is_valid():
            form.save()
            return redirect('indicadores:indicador_detalhes', pk=pk)
    else:
        form = IndicadorManNSAForm(instance=indicadorman)
    return render(request, 'indicadores/indicador_detalhes.html', {'form': form})

def indicadorman_edit_nivelsuposto(request, pk):
    indicadorman = get_object_or_404(IndicadorMan, pk=pk)
    if request.method == 'POST':
        form = IndicadorManNivelSupostoForm(request.POST, instance=indicadorman)
        if form.is_valid():
            form.save()
            return redirect('indicadores:indicador_detalhes', pk=pk)
    else:
        form = IndicadorManNivelSupostoForm(instance=indicadorman)
    return render(request, 'indicadores/indicador_detalhes.html', {'form': form})


def enviar_arquivo(request, pk):
    indicadorman = get_object_or_404(IndicadorMan, pk=pk)
    if request.method == 'POST':
        indicadorman.conteudo = request.FILES['conteudo']
        indicadorman.usuario_relatorio = request.user
        indicadorman.data_envio = timezone.now()
        indicadorman.save()
        return redirect('indicadores:indicador_detalhes', indicador_man_id=pk)
    return redirect('indicadores:indicador_detalhes', indicador_man_id=pk)



#
def apagar_conteudo(request, indicador_man_id):
    indicadorman = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    if not verificar_vinculo(request, indicadorman.curso.id):
        return redirect('usuarios:home')
    indicadorman.conteudo.delete()
    indicadorman.usuario_relatorio = None
    indicadorman.data_envio = None
    indicadorman.save()
    return redirect('indicadores:indicador_detalhes', indicador_man_id=indicadorman.id)


def baixar_conteudo(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    curso = indicador_man.curso
    if request.user.tipo_usuario in [Usuario.GERENCIADOR, Usuario.RELATOR]:
        response = HttpResponse(indicador_man.conteudo.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={indicador_man.conteudo.name}'
        return response
    elif request.user.tipo_usuario == Usuario.AVALIADOR:
        if curso.capa:
            merger = PdfMerger()  # Use PdfMerger em vez de PdfFileMerger
            merger.append(curso.capa.path)
            merger.append(indicador_man.conteudo.path)
            merged_pdf = BytesIO()
            merger.write(merged_pdf)
            merged_pdf.seek(0)
            response = HttpResponse(merged_pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={curso.nome}_com_capa.pdf'
            return response
        else:
            response = HttpResponse(indicador_man.conteudo.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={indicador_man.conteudo.name}'
            return response
    else:
        data = {'error': 'Você não tem permissão para baixar este conteúdo.'}
        return JsonResponse(data, status=403)



def verificar_vinculo(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.user == curso.gerenciador or (request.user.tipo_usuario == Usuario.RELATOR and request.user in curso.membros.all()):
        return True
    else:
        return False





