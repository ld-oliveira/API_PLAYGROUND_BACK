from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ['id', 'nome', 'idade', 'foto', 'descricao', 'usuario', 'criado_em']
        read_only_fields = ['usuario', 'criado_em']

    def get_usuario(self, obj):
        if obj.usuario:
            return {"id": obj.usuario.id, "username": obj.usuario.username}
        return None
