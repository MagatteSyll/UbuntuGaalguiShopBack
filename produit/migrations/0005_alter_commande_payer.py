# Generated by Django 4.0.2 on 2022-03-08 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0004_commande_payer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='payer',
            field=models.BooleanField(default=False),
        ),
    ]
