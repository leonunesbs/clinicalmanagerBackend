# Generated by Django 3.1.2 on 2020-11-28 15:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20201128_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='data_agendamento',
        ),
        migrations.AddField(
            model_name='agenda',
            name='hora_agendamento',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
