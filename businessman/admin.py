from django.contrib import admin
from .models import Companies, Documents, Metrics

# Register your models here.
admin.site.register(Companies)
admin.site.register(Documents)
admin.site.register(Metrics)