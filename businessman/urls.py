from django.urls import path, include
from . import views
urlpatterns = [
    path('register_company/', views.register_company, name="register_company"),
]
