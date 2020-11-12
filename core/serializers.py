from rest_framework import serializers
from core.models import Consulta, Disponibilidade, Paciente


class PacienteSerializer(serializers.ModelSerializer):
    data_de_nascimento = serializers.DateField(format='%d/%m/%Y')
    idade = serializers.CharField(read_only=True)

    class Meta:
        model = Paciente
        fields = '__all__'


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'


class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidade
        fields = '__all__'
