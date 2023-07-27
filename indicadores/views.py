from django.shortcuts import render, get_object_or_404, redirect
from .forms import NSAForm, NivelSupostoForm, ConteudoForm
from .models import IndicadorMan, IndicadorInfo
from PyPDF2 import PdfFileMerger
from usuarios.models import Usuario
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from cursos.models import Curso
from django.utils import timezone
from django.http import FileResponse

def indicador_detalhes(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    curso = indicador_man.curso
    nsa_form = NSAForm(request.POST or None, instance=indicador_man)
    nivel_suposto_form = NivelSupostoForm(request.POST or None, instance=indicador_man)
    conteudo_form = ConteudoForm(request.POST or None, request.FILES or None, instance=indicador_man)
    curso = indicador_man.curso
    if request.method == 'POST':
        if nsa_form.is_valid():
            nsa_form.save()
            return redirect('indicadores:indicador_detalhes', indicador_man_id=indicador_man.id)
        if nivel_suposto_form.is_valid():
            nivel_suposto_form.save()
            return redirect('indicadores:indicador_detalhes', indicador_man_id=indicador_man.id)
        if conteudo_form.is_valid():
            conteudo_form.save()
            return redirect('indicadores/indicador_detalhes', indicador_man_id=indicador_man.id)

    # Buscar manualmente o objeto IndicadorInfo relacionado
    indicador_info = IndicadorInfo.objects.get(pk=indicador_man.indicador_info_id)

    context = {
        'nsa_form': nsa_form,
        'nivel_suposto_form': nivel_suposto_form,
        'conteudo_form': conteudo_form,
        'indicador_man': indicador_man,
        'curso': curso,
        'nome_indicador': indicador_info.nome,
        'mensagem_aviso': indicador_info.mensagem_aviso,
        'tabela_conceitos': indicador_info.tabela_conceitos,
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



def verificar_vinculo(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.user == curso.gerenciador or (request.user.tipo_usuario == Usuario.RELATOR and request.user in curso.membros.all()):
        return True
    else:
        return False



def apagar_conteudo(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    if not verificar_vinculo(request, indicador_man.curso.id):
        return redirect('usuarios:home')
    indicador_man.conteudo.delete()
    indicador_man.usuario_relatorio = None
    indicador_man.data_envio = None
    indicador_man.save()
    return redirect('indicadores:indicador_detalhes', indicador_man_id=indicador_man.id)

def enviar_arquivo(request, indicador_man_id):
    indicador_man = get_object_or_404(IndicadorMan, pk=indicador_man_id)
    if not verificar_vinculo(request, indicador_man.curso.id):
        return redirect('usuarios:home')
    if request.method == 'POST':
        form = ConteudoForm(request.POST, request.FILES)
        if form.is_valid():
            indicador_man.conteudo = form.cleaned_data['relatorio']
            indicador_man.usuario_relatorio = request.user
            indicador_man.data_envio = timezone.now()
            indicador_man.save()
            return redirect('indicadores:indicador_detalhes', indicador_man_id=indicador_man.id)
    else:
        form = ConteudoForm()
    return render(request, 'indicadores/indicador_detalhes.html', {'form': form})