# Generated by Django 5.0.1 on 2024-01-31 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_agence_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='avisclient',
            name='status',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
