# Generated by Django 5.0.1 on 2024-01-31 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannier',
            name='sous_titre_bannier',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='bannier',
            name='texte_bannier',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='bannier',
            name='titre_bannier',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
