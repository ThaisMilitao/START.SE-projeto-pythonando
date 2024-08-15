# Generated by Django 5.1 on 2024-08-15 00:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('businessman', '0003_metrics'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('percentual', models.FloatField()),
                ('status', models.CharField(choices=[('AS', 'Aguardando assinatura'), ('PE', 'Proposta enviada'), ('PA', 'Proposta aceita'), ('PR', 'Proposta recusada')], default='AS', max_length=2)),
                ('selfie', models.FileField(blank=True, null=True, upload_to='selfie')),
                ('rg', models.FileField(blank=True, null=True, upload_to='rg')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='businessman.companies')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
