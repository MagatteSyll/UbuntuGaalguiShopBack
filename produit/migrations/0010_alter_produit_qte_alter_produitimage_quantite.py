# Generated by Django 4.0.2 on 2022-03-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0009_boutique_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='qte',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='produitimage',
            name='quantite',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
