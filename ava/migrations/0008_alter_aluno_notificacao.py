# Generated by Django 3.2.20 on 2023-08-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ava', '0007_aluno_notificacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='notificacao',
            field=models.CharField(blank=True, max_length=510),
        ),
    ]