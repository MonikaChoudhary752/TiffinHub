# Generated by Django 5.0.3 on 2024-03-29 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_vendor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vendor',
            new_name='VendorInformation',
        ),
    ]
