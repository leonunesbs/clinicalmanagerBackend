# Generated by Django 3.1.2 on 2020-10-30 16:28

from django.db import migrations, models
import django.db.models.deletion


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
            ],
        ),
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=125)),
                ('especialidade', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'profissionais',
            },
        ),
        migrations.CreateModel(
            name='Disponibilidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horário', models.DateTimeField()),
                ('is_disponível', models.BooleanField(default=True)),
                ('profissional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profissional')),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificação', models.TextField()),
                ('queixa_principal', models.TextField()),
                ('história_doença_atual', models.TextField()),
                ('história_patológica_pregressa', models.TextField()),
                ('história_familiar', models.TextField()),
                ('alergias', models.TextField()),
                ('medicações_uso_contínuo', models.TextField()),
                ('exame_físico', models.TextField()),
                ('hipótese_diagnóstica', models.TextField()),
                ('conduta', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('disponibilidade', models.OneToOneField(limit_choices_to={'is_disponível': True}, on_delete=django.db.models.deletion.CASCADE, to='core.disponibilidade')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.paciente')),
            ],
        ),
    ]
