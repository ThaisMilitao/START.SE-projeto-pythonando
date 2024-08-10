from django.urls import path, include
from . import views
urlpatterns = [
    path('register_company/', views.register_company, name="register_company"),
    path('list_companies/', views.list_companies, name="list_companies"),
    path('company/<int:id>', views.company, name="company"),
    path('add_doc/<int:id>', views.add_doc, name="add_doc"),
    path('delete_doc/<int:id>', views.delete_doc, name="delete_doc"),
    path('add_metrics/<int:id>', views.add_metrics, name="add_metrics"),
]
