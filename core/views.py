from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from .models import Colaborador, Consulta, Unidade, Prontuário
from .serializers import ConsultaSerializer, UnidadeSerializer, ProntuárioSerializier, ProntuárioDetalhadoSerializier


@api_view(['POST'])
def autenticar(request, format=None):
    usuário = request.data['usuário']
    senha = request.data['senha']

    if usuário and senha:
        user = authenticate(username=usuário, password=senha)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
    else:
        return Response({
            usuário: 'Este campo é obrigatório.',
            senha: 'Este campo é obrigatório.'
        }, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unidades_colaborador(request, format=None):
    unidades = Unidade.objects.all()

    unidades_return = []
    for unidade in unidades:
        for colaborador in unidade.colaboradores.all():
            if colaborador.user == request.user:
                unidades_return.append(unidade)

    serializer = UnidadeSerializer(unidades_return, many=True)

    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prontuários(request, unidadeId, format=None):
    unidade = get_object_or_404(Unidade, pk=unidadeId)

    if unidade.verificar_vínculo(request.user):
        prontuários = Prontuário.objects.all()
        serializer = ProntuárioSerializier(prontuários, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prontuário(request, unidadeId, prontuárioId, format=None):
    unidade = get_object_or_404(Unidade, pk=unidadeId)

    if unidade.verificar_vínculo(request.user):
        prontuário = get_object_or_404(Prontuário, pk=prontuárioId)
        serializer = ProntuárioDetalhadoSerializier(prontuário)

        return Response(serializer.data, status=HTTP_200_OK)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nova_consulta(request, unidadeId, prontuárioId, format=None):
    unidade = get_object_or_404(Unidade, pk=unidadeId)
    dados_clínicos = request.data['dados_clínicos']

    if unidade.verificar_vínculo(request.user):
        prontuário = get_object_or_404(Prontuário, pk=prontuárioId)
        consulta = Consulta.objects.create(
            prontuário=prontuário,
            responsável=Colaborador.objects.get(user=request.user),
            setor=prontuário.setor_atual,
            célula=prontuário.célula_atual,
            dados_clínicos=dados_clínicos
        )
        serializer = ConsultaSerializer(consulta)
        return Response(serializer.data, status=HTTP_201_CREATED)

    else:
        return Response(status=HTTP_401_UNAUTHORIZED)
