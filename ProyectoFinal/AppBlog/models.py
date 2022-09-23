from pyexpat import model
from django.db import models

    
class Categoria(models.Model):

    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f'Categoria {self.nombre}'


class Publicacion(models.Model):

    titulo = models.CharField(max_length=80)
    cuerpo = models.CharField(max_length=500)
    imagen = models.ImageField()
    fecha = models.DateTimeField()
    #categorias

    def __str__(self):
        return f'Publicación {self.titulo} de {self.fecha}'


class Mensaje(models.Model):

    remitente = models.CharField(max_length=50)
    destinatario = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=200)