# Generated by Django 5.1.6 on 2025-03-01 16:38

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_stockpricehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketevent',
            name='duration',
            field=models.PositiveIntegerField(default=60),
        ),
        migrations.AddField(
            model_name='marketevent',
            name='impact_factor',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=4),
        ),
    ]
