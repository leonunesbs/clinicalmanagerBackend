from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from core.views import *


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'paciente', PacienteViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'consulta', ConsultaViewSet)
router.register(r'prontuarios', ProntuárioViewSet)
router.register(r'prontuario', ProntuárioViewSet)
router.register(r'agendas', AgendaViewSet)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    path('agendamento/', agendamento, name='agendamento'),
    path('iniciar/', iniciar_consulta, name='iniciar_consulta'),
    path('cadastrar-prontuario/<int:id>/', cadastrar_prontuário,
         name='cadastrar_prontuário'),
]
