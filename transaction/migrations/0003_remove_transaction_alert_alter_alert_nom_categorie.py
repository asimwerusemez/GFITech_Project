# Generated by Django 5.0.6 on 2024-07-25 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_transaction_alert'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='alert',
        ),
        migrations.AlterField(
            model_name='alert',
            name='nom_categorie',
            field=models.CharField(max_length=300),
        ),
    ]
