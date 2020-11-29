# Generated by Django 3.1.2 on 2020-11-28 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20201128_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='confirmado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='agenda',
            name='data_agendamento',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
