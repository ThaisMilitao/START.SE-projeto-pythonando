from django.shortcuts import render, redirect
from .models import Companies
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def register_company(request):
    if request.method == "GET":
        return render(request, 'register_company.html', {'time_existence': Companies.time_existence_choices, 'areas': Companies.area_choices })
    elif request.method == "POST":
        name = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        time_existence = request.POST.get('tempo_existencia')
        description = request.POST.get('descricao')
        end_date = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        stage = request.POST.get('estagio')
        area = request.POST.get('area')
        target_audience = request.POST.get('publico_alvo')
        value = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')
        try:
            company = Companies(
            user=request.user,
            name=name,
            cnpj=cnpj,
            site=site,
            time_existence=time_existence,
            description=description,
            end_date_acquisition=end_date,
            percentual_equity=percentual_equity,
            stage=stage,
            area=area,
            target_audience=target_audience,
            value=value,
            pitch=pitch,
            logo=logo
            )
            company.save()
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/businessman/register_company')

    messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
    return redirect('/businessman/register_company')
