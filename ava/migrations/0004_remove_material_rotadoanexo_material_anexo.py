# Generated by Django 4.2.3 on 2023-07-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ava', '0003_material_nomedomaterial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='rotaDoAnexo',
        ),
        migrations.AddField(
            model_name='material',
            name='anexo',
            field=models.FileField(default='', upload_to='diretorio/'),
            preserve_default=False,
        ),
    ]