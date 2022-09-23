from django import forms

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