# Generated by Django 5.0.6 on 2024-05-18 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_especialista_coren_remove_especialista_cro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_especialista',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_paciente',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
