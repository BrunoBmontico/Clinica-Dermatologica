# Generated by Django 5.0.6 on 2024-05-30 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_alter_consulta_especialidade_alter_consulta_medico"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuario",
            name="is_paciente",
        ),
    ]
