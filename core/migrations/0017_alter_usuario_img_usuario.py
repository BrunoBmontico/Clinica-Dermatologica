# Generated by Django 5.0.6 on 2024-06-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_consulta_id_medico_alter_consulta_id_usuario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="Img_Usuario",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Imagem de Usuário"
            ),
        ),
    ]
