# Generated by Django 5.0.1 on 2024-05-08 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
