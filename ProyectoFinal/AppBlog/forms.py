from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FormRegistroUsuario(UserCreationForm):

    username = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita la contraseña', widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FormularioCategoria(forms.Form):

    nombre = forms.CharField()


class FormularioPublicacion(forms.Form):

    titulo = forms.CharField()
    cuerpo = forms.CharField()
    imagen = forms.ImageField()
    fecha = forms.DateTimeField()


class FormularioMensaje(forms.Form):

    remitente = forms.CharField()
    destinario = forms.CharField()
    mensaje = forms.CharField()