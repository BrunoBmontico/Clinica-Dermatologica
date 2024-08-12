# Generated by Django 5.0.6 on 2024-06-07 13:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_remove_usuario_is_paciente"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="consulta",
            name="Id_Paciente",
        ),
        migrations.AddField(
            model_name="consulta",
            name="Id_Usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
