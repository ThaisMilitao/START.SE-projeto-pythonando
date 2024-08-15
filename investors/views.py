from django.shortcuts import render, redirect
from businessman.models import Companies, Documents
from .models import InvestmentProposal
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
# Create your views here.
def suggestion(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    
    areas = Companies.area_choices
    if request.method == "GET":   
        return render(request, 'suggestion.html', {'areas': areas})
    elif request.method == "POST":
        type = request.POST.get('tipo')
        area = request.POST.getlist('area')
        value = request.POST.get('valor')

        if type == 'C':
            companies = Companies.objects.filter(time_existence='+5').filter(stage="E")
        elif type == 'D':
            companies = Companies.objects.filter(time_existence__in=['-6', '+6', '+1']).exclude(stage="E")
        
        companies = companies.filter(area__in=area)
        
        selected_companies = []
        for company in companies:
            percentual = (float(value) * 100) / float(company.valuation)
            if percentual >= 1:
                selected_companies.append(company)

        return render(request, 'suggestion.html', {'companies': selected_companies, 'areas': areas})

def company_details(request, id):
    company = Companies.objects.get(id=id)
    documents = Documents.objects.filter(company=company)
    investment_proposal = InvestmentProposal.objects.filter(company=company).filter(status='PA')
    percentage_sold = 0
    for ip in investment_proposal:
        percentage_sold += ip.percentual

    threshold = (80 * company.percentual_equity) / 100
    realized = False
    if percentage_sold >= threshold:
        realized = True
        
    available_percentage = company.percentual_equity - percentage_sold
    return render(request, 'company_details.html', {'company': company, 'documents':documents,
                                                    'percentage_sold':int(percentage_sold), 'realized':realized,
                                                    'available_percentage':available_percentage})

def make_proposal(request, id):
    value = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    company = Companies.objects.get(id=id)

    proposal_accepted = InvestmentProposal.objects.filter(company=company).filter(status='PA')
    total = 0

    for pa in proposal_accepted:
        total = total + pa.percentual

    if total + int(percentual)  > company.percentual_equity:
        messages.add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo.')
        return redirect(f'/investors/company_details/{id}')


    valuation = (100 * int(value)) / int(percentual)

    if valuation < (int(company.valuation) / 2):
        messages.add_message(request, constants.WARNING, f'Seu valuation proposto foi R${valuation} e deve ser no mínimo R${company.valuation/2}')
        return redirect(f'/investors/company_details/{id}')

    ip = InvestmentProposal(
        value = value,
        percentual = percentual,
        company = company,
        investor = request.user,
    )
    ip.save()

    #messages.add_message(request, constants.SUCCESS, f'Proposta enviada com sucesso')
    return redirect(f'/investors/sign_contract/{ip.id}')

def sign_contract(request, id):
    ip = InvestmentProposal.objects.get(id=id)
    if ip.status != "AS":
        raise Http404()
    
    if request.method == "GET":
        return render(request, 'sign_contract.html', {'ip': ip})
    elif request.method == "POST":
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')
        
        ip.selfie = selfie
        ip.rg = rg
        ip.status = 'PE'
        ip.save()

        messages.add_message(request, constants.SUCCESS, f'Contrato assinado com sucesso, sua proposta foi enviada a empresa.')
        return redirect(f'/investors/company_details/{ip.company.id}')
