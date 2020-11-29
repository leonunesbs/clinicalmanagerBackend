# Generated by Django 3.1.2 on 2020-11-29 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_agenda_auto_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='local_de_atendimento',
            field=models.CharField(default='Unimed Teresina', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agenda',
            name='auto_notified',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
