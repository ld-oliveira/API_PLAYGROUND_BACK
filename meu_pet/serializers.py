from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'nome', 'idade', 'foto', 'descricao', 'usuario', 'criado_em']
        read_only_fields = ['usuario', 'criado_em']