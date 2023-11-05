from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Produtos(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    preco = models.FloatField(default=False)
    tamanho = models.CharField(max_length=10, default=False)
    data_cadastro = models.DateTimeField(default=timezone.now)
    foto = models.ImageField(upload_to='produto')
    active = models.BooleanField(default=True)
    descricao = models.CharField(max_length=500, default='descricao')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome
