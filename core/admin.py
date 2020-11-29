from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *


def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


class AgendaAdmin(admin.ModelAdmin):
    def cancelar_agendamentos(modeladmin, request, queryset):
        for q in queryset:
            q.cancelar_agendamento()
    cancelar_agendamentos.short_description = "Cancelar agendamentos selecionados"
    list_display = [
        'profissional',
        'horário',
        'is_disponível',
        'hora_confirmação',
        'confirmado',
        'auto_notified',
        linkify(field_name='prontuário')
    ]
    actions = [cancelar_agendamentos]


class ConsultaAdmin(admin.ModelAdmin):
    list_display = [
        'get_paciente',
        'profissional',
        'início',
        'duração_consulta',
        'has_observações'
    ]


class ProntuárioAdmin(admin.ModelAdmin):
    list_display = [
        'paciente'
    ]


# Register your models here.
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Paciente)
admin.site.register(Profissional)
admin.site.register(Prontuário, ProntuárioAdmin)
