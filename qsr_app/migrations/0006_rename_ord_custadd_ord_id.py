# Generated by Django 4.2.6 on 2023-11-19 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qsr_app', '0005_custadd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='custadd',
            old_name='ord',
            new_name='ord_id',
        ),
    ]