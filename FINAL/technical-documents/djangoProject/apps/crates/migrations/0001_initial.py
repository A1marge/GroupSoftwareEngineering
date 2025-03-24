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
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('item_type', models.CharField(choices=[('material', 'Material'), ('blueprint', 'Blueprint'), ('special', 'Special Item'), ('consumable', 'Consumable'), ('currency', 'Currency'), ('Seed', 'Seed'), ('crop', 'Crop')], max_length=20)),
                ('rarity', models.IntegerField(choices=[(1, 'Common'), (2, 'Uncommon'), (3, 'Rare'), (4, 'Epic'), (5, 'Legendary'), (6, 'Mythic')], default=1)),
                ('rarity_multiplier', models.DecimalField(decimal_places=2, default=1.0, max_digits=5)),
                ('is_stackable', models.BooleanField(default=True)),
                ('base_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Crate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crate_type', models.CharField(choices=[('materials', 'Materials Crate'), ('advanced_materials', 'Advanced Materials Crate'), ('eco_tech', 'Eco-Tech Crate'), ('industrial', 'Industrial Crate'), ('green_construction', 'Green Construction Crate'), ('high_tech', 'High-Tech Crate'), ('blueprint', 'Blueprint Crate'), ('epic', 'Epic Crate'), ('rare_blueprint', 'Rare Blueprint Crate'), ('special', 'Special Crate'), ('mystery', 'Mystery Crate'), ('legendary', 'Legendary Crate'), ('eco', 'Eco Crate'), ('farm_currency', 'Farm Currency Crate'), ('plant_seed', 'Plant Seed Crate'), ('rare_seed', 'Rare Herb Crate'), ('exotic_seed', 'Exotic Flora Crate'), ('mythical_seed', 'Mythical Garden Crate'), ('legendary_seed', 'Legendary Botanical Crate')], default='materials', max_length=50)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency_type', models.CharField(choices=[('main', 'Main Currency'), ('farm', 'Farm Currency')], max_length=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('is_opened', models.BooleanField(default=False)),
                ('rewards', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CrateOpeningHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crate_type', models.CharField(max_length=50)),
                ('reward_item', models.CharField(max_length=100)),
                ('reward_rarity', models.IntegerField()),
                ('opened_at', models.DateTimeField(auto_now_add=True)),
                ('crate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crates.crate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crate_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crates.item')),
            ],
            options={
                'unique_together': {('user', 'item')},
            },
        ),
    ]
