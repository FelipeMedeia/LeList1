from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Produtos(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    data_validade = models.DateField()
    foto = models.ImageField(upload_to='produto')
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

