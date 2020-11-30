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

from core.models import Consulta, Agenda, Paciente, Profissional, Prontuário
from core.serializers import ConsultaSerializer, PacienteSerializer, AgendaSerializer, ProfissionalSerializer, ProntuárioSerializer, serializers


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


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


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


@api_view(['GET'])
def listar_agendas(request):
    agendas = Agenda.objects.all()

    serializer = AgendaSerializer(agendas, many=True)

    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
def nova_agenda(request):
    profissional = request.data.get('profissional')
    local_de_atendimento = request.data.get('localDeAtendimento')
    start = request.data.get('start')
    end = request.data.get('end')

    if (profissional and start and end):
        agenda, _ = Agenda.objects.get_or_create(
            profissional=Profissional.objects.get(pk=1),
            local_de_atendimento=local_de_atendimento,
            horário_start=start,
            horário_end=end
        )
        serializer = AgendaSerializer(agenda)
        return Response(serializer.data, status=HTTP_200_OK)

    else:
        return Response({'profissional': 'number', 'start': 'Date', 'end': 'Date'}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def agendar_prontuário(request):
    agenda_id = request.data.get('agenda')
    prontuário_id = request.data.get('prontuário')

    if (prontuário_id and agenda_id):
        agenda = Agenda.objects.get(pk=agenda_id)
        agenda.prontuário = Prontuário.objects.get(
            pk=prontuário_id
        )
        agenda.save()
        serializer = AgendaSerializer(agenda)
        return Response(serializer.data, status=HTTP_200_OK)

    else:
        return Response({'prontuário': 'number'}, status=HTTP_400_BAD_REQUEST)
