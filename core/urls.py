from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from core.views import ConsultaViewSet, DisponibilidadeViewSet, PacienteViewSet, agendamento


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'paciente', PacienteViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'consulta', ConsultaViewSet)
router.register(r'disponibilidade', DisponibilidadeViewSet)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('agendamento/', agendamento, name='agendamento'),
]
