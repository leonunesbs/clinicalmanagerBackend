from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings
from rest_framework import response
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class Paciente(models.Model):
    nome = models.CharField(max_length=125)
    data_de_nascimento = models.DateField()
    cpf = models.CharField(max_length=15)
    rg = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)

    class Meta:
        ordering = ['nome']

    def idade(self):
        return ((timezone.now().date() - self.data_de_nascimento).days//366)

    def notify(self, msg):
        from twilio.rest import Client
        import re

        try:
            account_sid = settings.TWILIO_ACC_SID
            auth_token = settings.TWILIO_AUTH_TOKEN

            client = Client(account_sid, auth_token)

            clean_telefone = re.compile(
                r'[^\d.]+').sub('', self.telefone)

            clean_telefone = clean_telefone.replace(clean_telefone[2], '')

            client.messages.create(
                from_='whatsapp:+14155238886',
                body=msg,
                to=f'whatsapp:+55{clean_telefone}'
            )
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        return super().save(*args, **kwargs)


class Profissional(models.Model):
    nome = models.CharField(max_length=125)
    especialidade = models.CharField(max_length=30)
    registro = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'profissionais'

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    id = models.AutoField(primary_key=True)
    profissional = models.ForeignKey('Profissional', on_delete=models.CASCADE)
    local_de_atendimento = models.CharField(
        max_length=30, blank=True, null=True)
    horário_start = models.DateTimeField()
    horário_end = models.DateTimeField()
    is_disponível = models.BooleanField(default=True)
    prontuário = models.ForeignKey(
        'Prontuário', blank=True, null=True, on_delete=models.CASCADE)
    hora_confirmação = models.DateTimeField(editable=False, null=True)
    confirmado = models.BooleanField(default=False)

    auto_notified = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ['-horário_start']

    def __str__(self):
        if self.is_disponível:
            disp = 'ON'
        else:
            disp = 'OFF'
        return f'{disp} {self.profissional} [{self.horário_start.strftime("%d/%m/%Y às %Hh%M")}]'

    def notify_consulta_marcada(self):
        def get_horário_display():
            today = timezone.now()
            start = self.horário_start - timedelta(hours=3)
            if start.day == today.day:
                return f'HOJE, {start.strftime("%d/%m/%Y às %Hh%M")}'
            if start.day == today.day + 1:
                return f'AMANHÃ, {start.strftime("%d/%m/%Y às %Hh%M")}'
            return f'{start.strftime("%d/%m/%Y às %Hh%M")}'

        self.prontuário.paciente.notify(
            f'Olá {self.prontuário.paciente.nome.split()[0]}!\nSua consulta está marcada para {get_horário_display()} - {self.local_de_atendimento}.')

    def solicitar_confirmação(self):
        def get_horário_display():
            today = timezone.now()
            if self.horário_start.day == today.day:
                return f'HOJE, {self.horário_start.strftime("%d/%m/%Y às %Hh%M")}'
            if self.horário_start.day == today.day + 1:
                return f'AMANHÃ, {self.horário_start.strftime("%d/%m/%Y às %Hh%M")}'

            return f'{self.horário_start.strftime("%d/%m/%Y às %Hh%M")}'

        if self.prontuário:
            self.prontuário.paciente.notify(
                f'Olá {self.prontuário.paciente.nome.split()[0]}!\nVocê deseja CONFIRMAR a sua consulta que está marcada para {get_horário_display()} - {self.local_de_atendimento}?')

        return 'ok'

    def confirmar_agendamento(self):
        self.confirmado = True
        self.hora_confirmação = timezone.now()
        self.save()

    def cancelar_agendamento(self):
        self.prontuário = None
        self.is_disponível = True
        self.confirmado = False
        self.auto_notified = False
        self.save()

    def auto_notify(self):
        if not self.auto_notified:
            self.notify_consulta_marcada()
            self.auto_notified = True
            self.save()

    def save(self, *args, **kwargs):
        if self.prontuário:
            self.is_disponível = False
            self.auto_notify()

        if self.confirmado:
            self.data_agendamento = timezone.now()

        if self.is_disponível:
            self.prontuário = None

        super().save(*args, **kwargs)

    def agendar(self, prontuário):
        self.prontuário = prontuário
        return self.save()

    def agendar(self, prontuário):
        self.prontuário = prontuário
        return self.save()


class Prontuário(models.Model):
    paciente = models.OneToOneField('Paciente', on_delete=models.CASCADE)

    def __str__(self):
        return self.paciente.nome

    def get_data_de_nascimento(self):
        return self.paciente.data_de_nascimento


class Consulta(models.Model):
    prontuário = models.ForeignKey('Prontuário', on_delete=models.CASCADE)
    profissional = models.ForeignKey(
        'Profissional', on_delete=models.SET_NULL, null=True)

    caso_clínico = models.TextField(editable=False)

    observações = models.TextField(blank=True)

    início = models.DateTimeField(default=timezone.now)
    fim = models.DateTimeField()

    def duração_consulta(self):
        if (self.início and self.fim):
            return f'{(self.fim - self.início).seconds // 60}min{(self.fim - self.início).seconds % 60}s'
        else:
            return False

    def has_observações(self):
        if self.observações:
            return True
        else:
            return False

    def iniciar(self):
        self.início = timezone.now()
        return self.save()

    def finalizar(self):
        self.fim = timezone.now()
        return self.save(), self.duração_consulta()

    def get_paciente(self):
        return self.prontuário.paciente

    def __str__(self):
        return self.prontuário.paciente.nome

    has_observações.boolean = True
    get_paciente.short_description = 'paciente'
