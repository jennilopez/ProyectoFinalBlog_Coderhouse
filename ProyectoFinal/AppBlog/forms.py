from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class FormRegistroUsuario(UserCreationForm):

    username = forms.CharField(label='Nombre de usuario')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.EmailField(label='Correo electrónico')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita la contraseña', widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['username', 'first_name','last_name', 'email', 'password1', 'password2']


class FormEditarUsuario(UserCreationForm):

    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    password1 = forms.CharField(label='Ingrese una contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita la contraseña',widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['email', 'first_name','last_name', 'password1', 'password2']


class FormEditarPerfil(forms.ModelForm):
    
    avatar = forms.ImageField(required=False)
    biografia = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}))

    class Meta:
        model = UserProfile
        fields = ['avatar','biografia']


class FormCrearCategoria(forms.Form):

    nombre = forms.CharField()
