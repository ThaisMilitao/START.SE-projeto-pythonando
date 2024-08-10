from django.shortcuts import render
from businessman.models import Companies

# Create your views here.
def suggestion(request):
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
