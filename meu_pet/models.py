from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage  # 👈 IMPORTANTE

class Animal(models.Model):
    nome = models.CharField(max_length=30)
    idade = models.IntegerField()
    foto = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='fotos_animais')
    descricao = models.TextField(max_length=350)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    is_generico = models.BooleanField(default=False)

    def __str__(self):
        if self.usuario:
            return f"{self.nome} ({self.usuario.username})"
        return f"{self.nome} (genérico)"
