# Generated by Django 3.1.4 on 2022-06-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220628_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
