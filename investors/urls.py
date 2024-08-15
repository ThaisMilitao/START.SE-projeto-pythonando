from django.urls import path
from . import views

urlpatterns = [
    path('suggestion/', views.suggestion, name="suggestion"),
    path('company_details/<int:id>', views.company_details, name="company_details"),
    path('make_proposal/<int:id>', views.make_proposal, name="make_proposal"),
    path('sign_contract/<int:id>', views.sign_contract, name="sign_contract"),
]