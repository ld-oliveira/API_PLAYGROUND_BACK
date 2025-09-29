from rest_framework import generics, permissions
from .models import Animal
from .serializers import AnimalSerializer

class AnimalListCreateView(generics.ListCreateAPIView):
    queryset = Animal.objects.all ()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #apenas quem está logado modifica
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)