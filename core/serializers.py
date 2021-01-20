from rest_framework import serializers
from .models import Unidade, Prontuário, Paciente, Consulta


class UnidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unidade
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class ProntuárioSerializier(serializers.ModelSerializer):
    paciente = serializers.CharField()
    unidade = serializers.CharField()

    class Meta:
        model = Prontuário
        fields = '__all__'


class ConsultaSerializer(serializers.ModelSerializer):
    responsável = serializers.CharField()
    setor = serializers.CharField()

    class Meta:
        model = Consulta
        fields = '__all__'


class ProntuárioDetalhadoSerializier(serializers.ModelSerializer):
    paciente = PacienteSerializer()
    unidade = serializers.CharField()
    histórico_clínico = ConsultaSerializer(many=True)

    class Meta:
        model = Prontuário
        fields = '__all__'
