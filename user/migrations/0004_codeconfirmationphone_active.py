# Generated by Django 4.0.2 on 2022-03-14 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_notification_nature_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeconfirmationphone',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]