from django.urls import path
from . import views

urlpatterns = [
    path('suggestion/', views.suggestion, name="suggestion"),
]