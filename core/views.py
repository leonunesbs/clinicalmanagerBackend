from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.shortcuts import get_object_or_404

from core.models import Consulta, Agenda, Paciente, Prontuário
from core.serializers import ConsultaSerializer, PacienteSerializer, AgendaSerializer, ProntuárioSerializer, serializers


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    # permission_classes = IsAdminUser


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer


class ProntuárioViewSet(viewsets.ModelViewSet):
    queryset = Prontuário.objects.all()
    serializer_class = ProntuárioSerializer


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer


@api_view(['POST'])
@permission_classes([])
def agendamento(request):
    data = {}
    try:
        data = {
            'disponibilidade': request.data['disponibilidade'],
            'paciente': request.data['paciente']
        }
    except KeyError as e:
        data = {
            'detail': f'Missing field: {e}'
        }
        return Response(data, status=HTTP_400_BAD_REQUEST)

    for d in data.items():
        key = d[0]
        value = d[1]
        if not value:
            data[key] = "Este campo é obrigatório."

    try:
        disponibilidade = Agenda.objects.get(
            pk=data['disponibilidade'])
        paciente = Paciente.objects.get(
            pk=data['paciente'])

        consulta = ''
        created = ''
        if request.method == 'POST':
            consulta, created = Consulta.agendar(
                disp=disponibilidade, pct=paciente)
        elif request.method == 'GET':
            consulta = Consulta.objects.get(
                disponibilidade=disponibilidade, paciente=paciente)

        serializer = ConsultaSerializer(consulta)
    except Exception as e:
        data = {
            'detail': f'{e}'
        }
        return Response(data, status=HTTP_400_BAD_REQUEST)
    if created:
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
def cadastrar_prontuário(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if paciente:
        prontuario, _ = Prontuário.objects.get_or_create(paciente=paciente)
        serializer = ProntuárioSerializer(prontuario)

        return Response(serializer.data, status=HTTP_201_CREATED)

    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
def iniciar_consulta(request):
    Consulta.objects.get(id=1).iniciar()


@api_view(['POST'])
def testando(request):

    if request.data['Body'].lower() in ['sim', 's', 'yes', 'ok', 'confirmar']:
        paciente = Paciente.objects.get(nome='LEONARDO NUNES BEZERRA SOUZA')
        paciente.notify(f'Sua consulta foi confirmada.')
        agenda = Agenda.objects.get(prontuário__paciente=paciente)
        agenda.confirmar_agendamento()
