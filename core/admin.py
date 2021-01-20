from django.contrib import admin
from .models import *


class UnidadeAdmin(admin.ModelAdmin):
    filter_horizontal = ['colaboradores']


admin.site.register(Colaborador)
admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Setor)
admin.site.register(Célula)
admin.site.register(Paciente)
admin.site.register(Prontuário)
admin.site.register(Consulta)
admin.site.register(ExameProcedimento)
admin.site.register(Prescrição)

# Register your models here.
