# Generated by Django 3.1.2 on 2020-11-30 18:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=125)),
                ('data_de_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=15)),
                ('rg', models.CharField(max_length=20)),
                ('telefone', models.CharField(max_length=15)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=125)),
                ('especialidade', models.CharField(max_length=30)),
                ('registro', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'profissionais',
            },
        ),
        migrations.CreateModel(
            name='Prontuário',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caso_clínico', models.TextField(editable=False)),
                ('observações', models.TextField(blank=True)),
                ('início', models.DateTimeField(default=django.utils.timezone.now)),
                ('fim', models.DateTimeField()),
                ('profissional', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.profissional')),
                ('prontuário', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.prontuário')),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('horário_start', models.DateTimeField()),
                ('horário_end', models.DateTimeField()),
                ('is_disponível', models.BooleanField(default=True)),
                ('hora_confirmação', models.DateTimeField(editable=False, null=True)),
                ('confirmado', models.BooleanField(default=False)),
                ('auto_notified', models.BooleanField(default=False, editable=False)),
                ('profissional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profissional')),
                ('prontuário', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.prontuário')),
            ],
            options={
                'ordering': ['-horário_start'],
            },
        ),
    ]
