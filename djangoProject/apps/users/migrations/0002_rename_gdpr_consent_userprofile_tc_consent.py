# Generated by Django 5.1.6 on 2025-02-27 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='gdpr_consent',
            new_name='tc_consent',
        ),
    ]
