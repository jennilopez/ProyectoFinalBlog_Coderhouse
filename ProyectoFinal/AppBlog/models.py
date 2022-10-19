from enum import unique
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatares', null=True, blank=True, default='avatares/avatardefault.png')
    biografia = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

    
class Categoria(models.Model):

    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.nombre}'


class EntradaBlog(models.Model):

    titulo = models.CharField(max_length=80)
    subtitulo = models.CharField(max_length=100)
    cuerpo = RichTextField(verbose_name='Contenido')
    imagen = models.ImageField(upload_to='posteos')
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Publicación {self.titulo} de {self.fecha}'
