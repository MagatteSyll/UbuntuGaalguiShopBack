# Generated by Django 4.0.2 on 2022-03-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0007_alter_produit_vendu_qte'),
    ]

    operations = [
        migrations.AddField(
            model_name='boutique',
            name='avertissement',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
