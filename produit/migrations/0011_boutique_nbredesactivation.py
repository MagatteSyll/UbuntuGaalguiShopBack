# Generated by Django 4.0.2 on 2022-03-12 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0010_alter_produit_qte_alter_produitimage_quantite'),
    ]

    operations = [
        migrations.AddField(
            model_name='boutique',
            name='nbredesactivation',
            field=models.PositiveIntegerField(default=0),
        ),
    ]