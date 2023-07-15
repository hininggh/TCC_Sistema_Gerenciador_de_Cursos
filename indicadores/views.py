from django.shortcuts import render, get_object_or_404, redirect
from .forms import NSAForm, NivelSupostoForm, RelatorioForm
from .models import IndicadorMan

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