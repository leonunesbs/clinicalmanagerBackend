from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Colaborador(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')
    nome = models.CharField(max_length=25, blank=True, null=True)
    função = models.CharField(max_length=25, blank=True, null=True)
    registro = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'colaboradores'

    def __str__(self) -> str:
        return self.nome


class Unidade(models.Model):
    nome = models.CharField(max_length=50)
    colaboradores = models.ManyToManyField('Colaborador', blank=True)

    def __str__(self) -> str:
        return self.nome

    def verificar_vínculo(self, user: models.Model):
        for colaborador in self.colaboradores.all():
            if colaborador.user == user:
                return True
        return False


class Setor(models.Model):
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE)
    nome = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'setores'

    def __str__(self) -> str:
        return self.nome


class Célula(models.Model):
    setor = models.ForeignKey('Setor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=15)
    prontuário = models.ForeignKey(
        'Prontuário', on_delete=models.SET_NULL, blank=True, null=True, related_name='prontuário')


class Paciente(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nome


class Anexo(models.Model):
    prontuário = models.ForeignKey('Prontuário', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Consulta(Anexo):
    responsável = models.ForeignKey(
        'Colaborador', on_delete=models.SET_NULL, blank=True, null=True)
    setor = models.ForeignKey('Setor', on_delete=models.SET_NULL,
                              blank=True, null=True)
    célula = models.ForeignKey(
        'Célula', on_delete=models.SET_NULL, blank=True, null=True)
    data_hora = models.DateTimeField(default=timezone.now)
    dados_clínicos = models.TextField()

    class Meta:
        ordering = ['-data_hora']


class Prontuário(models.Model):
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE)
    paciente = models.ForeignKey(
        'Paciente', on_delete=models.SET_NULL, blank=True, null=True)
    setor_atual = models.ForeignKey(
        'Setor', on_delete=models.SET_NULL, blank=True, null=True, related_name='setor_atual')
    célula_atual = models.ForeignKey(
        'Célula', on_delete=models.SET_NULL, blank=True, null=True, related_name='célula_atual')

    def histórico_clínico(self):
        consultas = Consulta.objects.filter(prontuário=self.pk)
        return consultas


class ExameProcedimento(Anexo):
    solicitante = models.ForeignKey(
        'Colaborador', on_delete=models.SET_NULL, blank=True, null=True, related_name='solicitante')
    nome = models.CharField(max_length=30)

    responsável = models.ForeignKey(
        'Colaborador', on_delete=models.SET_NULL, blank=True, null=True, related_name='responsável')
    resultado = models.TextField(blank=True, null=True)

    status = models.CharField(default='SOLICITADO', max_length=20)
    último_status = models.DateTimeField(default=timezone.now)

    data_solicitado = models.DateTimeField(default=timezone.now)
    data_resultado = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'exame/procedimento'
        verbose_name_plural = 'exames/procedimentos'


class Prescrição(Anexo):
    prescritor = models.ForeignKey(
        'Colaborador', blank=True, null=True, on_delete=models.SET_NULL, related_name='prescritor')
    data_prescrição = models.DateField()
    prescrição = models.TextField()

    class Meta:
        verbose_name_plural = 'prescrições'
