from django.shortcuts import render, redirect
from .models import Companies, Documents, Metrics
from investors.models import InvestmentProposal
from django.contrib import messages
from django.contrib.messages import constants


# Create your views here.
def register_company(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
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

def list_companies(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    if request.method == "GET":
        companies = Companies.objects.filter(user=request.user)
        return render(request, 'list_companies.html', {'companies': companies})
     
def company(request, id):    
    company = Companies.objects.get(id=id)

    if company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect(f'/businessman/list_companies')
    
    if request.method == "GET":
        documents = Documents.objects.filter(company=company)
        investment_proposal = InvestmentProposal.objects.filter(company=company)
        
        percentage_sold = 0
        for ip in investment_proposal:
            if ip.status == 'PA':
                percentage_sold += ip.percentual
        
        total_raised = sum(investment_proposal.filter(status='PA').values_list('value', flat=True))
        current_valuation = (100 * float(total_raised)) / float(percentage_sold) if percentage_sold != 0 else 0
        investment_proposal_sent = investment_proposal.filter(status='PE')
        return render(request, 'company.html', {'company': company, 'documents': documents, 
                                                'investment_proposal_sent': investment_proposal_sent,
                                                'percentage_sold':int(percentage_sold),
                                                'total_raised':total_raised,
                                                'current_valuation':current_valuation})
    
def add_doc(request, id):
    company = Companies.objects.get(id=id)
    title = request.POST.get('titulo')
    file = request.FILES.get('arquivo')
    extension = file.name.split('.')

    if company.user != request.user:
        messages.add_message(request, constants.ERROR, "Essa empresa não é sua")
        return redirect(f'/businessman/list_companies')

    if extension[1] != 'pdf':
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect(f'/businessman/company/{company.id}')
    
    if not file:
        messages.add_message(request, constants.ERROR, "Envie um arquivo")
        return redirect(f'/businessman/company/{company.id}')
        
    document = Documents(
        company=company,
        title=title,
        file=file
    )
    document.save()
    messages.add_message(request, constants.SUCCESS, "Arquivo cadastrado com sucesso")
    return redirect(f'/businessman/company/{company.id}')

def delete_doc(request, id):
    document = Documents.objects.get(id=id)
    if document.company.user != request.user:
        messages.add_message(request, constants.ERROR, "Esse documento não é seu")
        return redirect(f'/businessman/company/{document.company.id}')

    document.delete()
    messages.add_message(request, constants.SUCCESS, "Documento excluído com sucesso")
    return redirect(f'/businessman/company/{document.company.id}')

def add_metrics(request, id):
    company = Companies.objects.get(id=id)
    title = request.POST.get('titulo')
    value = request.POST.get('valor')
    
    metric = Metrics(
        company=company,
        title=title,
        value=value
    )
    metric.save()

    messages.add_message(request, constants.SUCCESS, "Métrica cadastrada com sucesso")
    return redirect(f'/businessman/company/{company.id}')


def manage_proposal(request, id):
    action = request.GET.get('action')
    ip = InvestmentProposal.objects.get(id=id)

    if action == 'accept':
        messages.add_message(request, constants.SUCCESS, 'Proposta aceita')
        ip.status = 'PA'
    elif action == 'deny':
        messages.add_message(request, constants.SUCCESS, 'Proposta recusada')
        ip.status = 'PR'


    ip.save()
    return redirect(f'/businessman/company/{ip.company.id}')
