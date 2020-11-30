from rest_framework import serializers
from core.models import Consulta, Agenda, Paciente, Prontuário, Profissional


class PacienteSerializer(serializers.ModelSerializer):
    data_de_nascimento = serializers.DateField(format='%Y-%m-%d')
    data_de_nascimento_local_format = serializers.DateField(
        format='%d/%m/%Y', source='data_de_nascimento', read_only=True)
    idade = serializers.CharField(read_only=True)

    class Meta:
        model = Paciente
        fields = '__all__'


class ProfissionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profissional
        fields = '__all__'


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = '__all__'


class ProntuárioSerializer(serializers.ModelSerializer):
    paciente = serializers.CharField(read_only=True)
    data_de_nascimento = serializers.DateField(
        source='get_data_de_nascimento', read_only=True)

    class Meta:
        model = Prontuário
        fields = ['id', 'paciente', 'data_de_nascimento']


class AgendaSerializer(serializers.ModelSerializer):
    profissional = ProfissionalSerializer()
    prontuário = ProntuárioSerializer()

    class Meta:
        model = Agenda
        fields = '__all__'
