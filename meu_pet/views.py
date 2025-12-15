from rest_framework import generics, permissions, parsers
from .models import Animal
from .serializers import AnimalSerializer

class AnimalListCreateView(generics.ListCreateAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        LIMITE = 60

        reais = list(
            Animal.objects.filter(is_generico=False).order_by("-criado_em")[:LIMITE]
        )

        faltam = LIMITE - len(reais)

        if faltam > 0:
            genericos = list(
                Animal.objects.filter(is_generico=True).order_by("-criado_em")[:faltam]
            )
        else:
            genericos = []

        # Reais primeiro, depois genéricos, total = 60
        return reais + genericos

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)



class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        from rest_framework.permissions import SAFE_METHODS
        if self.request.method in SAFE_METHODS:
            return Animal.objects.all()
        if self.request.user.is_authenticated:
            return Animal.objects.filter(usuario=self.request.user)
        return Animal.objects.none()

