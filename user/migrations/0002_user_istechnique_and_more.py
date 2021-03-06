# Generated by Django 4.0.2 on 2022-03-10 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='istechnique',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='nature_notification',
            field=models.CharField(blank=True, choices=[('avertissement', 'avertissement'), ('etat commande', 'etat commande'), ('vente', 'vente'), ('annulation d achat', 'annulation d achat'), ('annulation de vente', 'annulation de vente'), ('desactivation boutique', 'desactivation boutique'), ('pour follower', 'pour follower'), ('note vendeur', 'note vendeur'), ('reactivation boutique', 'reactivation boutique')], max_length=255),
        ),
    ]
