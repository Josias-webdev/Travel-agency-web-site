# Generated by Django 5.0.1 on 2024-03-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_avisclient_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='r_provenance',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
