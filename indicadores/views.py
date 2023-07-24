from django.shortcuts import render, get_object_or_404, redirect
from .forms import NSAForm, NivelSupostoForm, RelatorioForm
from .models import IndicadorMan
from django.http import FileResponse
from PyPDF2 import PdfFileMerger
from usuarios.models import Usuario
from django.http import HttpResponse, JsonResponse
from io import BytesIO



def indicador_detalhes(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    nsa_form = NSAForm(request.POST or None, instance=indicador_man)
    nivel_suposto_form = NivelSupostoForm(request.POST or None, instance=indicador_man)
    relatorio_form = RelatorioForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if nsa_form.is_valid():
            nsa_form.save()
            return redirect('indicador_detalhes', indicador_man_id=indicador_man.id)
        if nivel_suposto_form.is_valid():
            nivel_suposto_form.save()
            return redirect('indicador_detalhes', indicador_man_id=indicador_man.id)
        if relatorio_form.is_valid() and 'relatorio' in request.FILES:
            indicador_man.relatorio.save(request.FILES['relatorio'].name, request.FILES['relatorio'])
            return redirect('indicador_detalhes', indicador_man_id=indicador_man.id)
    context = {
        'nsa_form': nsa_form,
        'nivel_suposto_form': nivel_suposto_form,
        'relatorio_form': relatorio_form,
        'indicador_man': indicador_man,
    }
    return render(request, 'indicadores/indicador_detalhes.html', context)


def baixar_conteudo(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    curso = indicador_man.curso
    if request.user.tipo_usuario in [Usuario.GERENCIADOR, Usuario.RELATOR]:
        response = HttpResponse(indicador_man.conteudo.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={indicador_man.conteudo.name}'
        return response
    elif request.user.tipo_usuario == Usuario.AVALIADOR:
        if curso.capa:
            merger = PdfFileMerger()
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