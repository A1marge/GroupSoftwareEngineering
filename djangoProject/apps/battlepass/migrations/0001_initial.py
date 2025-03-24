# Generated by Django 5.1.5 on 2025-03-17 15:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BattlePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('season_number', models.IntegerField(unique=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('max_tiers', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='BattlePassTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier_level', models.IntegerField()),
                ('reward_name', models.CharField(max_length=255)),
                ('reward_type', models.CharField(choices=[('currency', 'Currency'), ('item', 'Item'), ('badge', 'Badge')], max_length=50)),
                ('reward_value', models.IntegerField()),
                ('is_premium', models.BooleanField(default=False)),
                ('battle_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battlepass.battlepass')),
            ],
        ),
        migrations.CreateModel(
            name='UserBattlePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_tier', models.IntegerField(default=0)),
                ('progress_points', models.IntegerField(default=0)),
                ('has_premium', models.BooleanField(default=False)),
                ('battle_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='battlepass.battlepass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
