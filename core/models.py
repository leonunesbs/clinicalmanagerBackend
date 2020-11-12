from django.db import models
from django.utils import timezone


class Paciente(models.Model):
    nome = models.CharField(max_length=125)
    data_de_nascimento = models.DateField()
    cpf = models.CharField(max_length=15)
    rg = models.CharField(max_length=20)

    class Meta:
        ordering = ['nome']

    def idade(self):
        return ((timezone.now().date() - self.data_de_nascimento).days//366)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)


class Profissional(models.Model):
    nome = models.CharField(max_length=125)
    especialidade = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'profissionais'

    def __str__(self):
        return self.nome


class Disponibilidade(models.Model):
    profissional = models.ForeignKey('Profissional', on_delete=models.CASCADE)
    horário = models.DateTimeField()
    is_disponível = models.BooleanField(default=True)

    def __str__(self):
        if self.is_disponível:
            disp = 'ON'
        else:
            disp = 'OFF'
        return f'{disp} {self.profissional} [{self.horário.strftime("%d/%m/%Y às %Hh%M")}]'

    def adicionar(profissional, horário):
        disponibilidade, _ = Disponibilidade.objects.get_or_create(
            profissional=profissional,
            horário=horário
        )
        return disponibilidade


class Consulta(models.Model):
    disponibilidade = models.OneToOneField(
        'Disponibilidade', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)

    identificação = models.TextField()
    queixa_principal = models.TextField()
    história_doença_atual = models.TextField()
    história_patológica_pregressa = models.TextField()
    história_familiar = models.TextField()
    alergias = models.TextField()
    medicações_uso_contínuo = models.TextField()
    exame_físico = models.TextField()

    hipótese_diagnóstica = models.TextField()
    conduta = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)

    def agendar(disp: models.Model, pct: models.Model):
        consulta, created = Consulta.objects.get_or_create(
            disponibilidade=disp,
            paciente=pct
        )
        consulta.disponibilidade.is_disponível = False
        consulta.disponibilidade.save()

        consulta.save()
        return (consulta, created)

    def remarcar(self, disp: models.Model):
        self.disponibilidade = disp
        self.disponibilidade.save()
        return self.disponibilidade

    def cancelar(self):
        self.disponibilidade.is_disponível = True
        self.disponibilidade.save()
        self.delete()

    def __str__(self):
        return f'{self.paciente.nome}'
