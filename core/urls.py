from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from core.views import *


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'paciente', PacienteViewSet)


app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    path('autenticar/', autenticar, name='autenticar'),
    path('unidades_colaborador/', unidades_colaborador,
         name='unidades_colaborador'),
    path('prontuarios/<int:unidadeId>/', prontuários, name='prontuários'),
    path('prontuario/<int:unidadeId>/<int:prontuárioId>/',
         prontuário, name='prontuário'),
    path('nova_consulta/<int:unidadeId>/<int:prontuárioId>/',
         nova_consulta, name='nova_consulta'),

]
