from django.db import models
from django.contrib.auth.models import User
from businessman.models import Companies
# Create your models here.
class InvestmentProposal(models.Model):
    status_choices = (
        ('AS', 'Aguardando assinatura'),
        ('PE', 'Proposta enviada'),
        ('PA', 'Proposta aceita'),
        ('PR', 'Proposta recusada')
    )
    value = models.DecimalField(max_digits=9, decimal_places=2)
    percentual = models.FloatField()
    company = models.ForeignKey(Companies, on_delete=models.DO_NOTHING)
    investor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=status_choices, default='AS')
    selfie = models.FileField(upload_to="selfie", null=True, blank=True)
    rg = models.FileField(upload_to="rg", null=True, blank=True)

    def __str__(self):
        return str(self.value)
    
def valuation(self):
    return (100*float(self.value)) / float(self.percentual)