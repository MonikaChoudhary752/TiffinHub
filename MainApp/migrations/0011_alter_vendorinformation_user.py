# Generated by Django 5.0.3 on 2024-03-30 05:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0010_vendorinformation_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorinformation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='vendor_information', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
