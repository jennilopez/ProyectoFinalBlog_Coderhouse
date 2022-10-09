from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from AppBlog.models import *
from AppBlog.forms import *

def inicio(request):
    return render(request, 'AppBlog/inicio.html')


def registroUsuario(request):

    if request.method=="POST":
        form = FormRegistroUsuario(request.POST)
        if form.is_valid():
            nombreUsuario = form.cleaned_data["username"]
            form.save()
            return render(request, "AppBlog/inicio.html", {"mensaje": f"Bienvenido @{nombreUsuario}!!"})
    else:
        form = FormRegistroUsuario()
    
    return render(request, "AppBlog/usuario.html", {"form":form, 'titulo':'Registro de usuario', 'submit':'Registrarse'})


def iniciarSesion(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contra)
            if user:
                login(request, user)
                return render(request, 'AppBlog/inicio.html', {'mensaje':f'Hola {user}'})
    else:
        form = AuthenticationForm()

    return render(request, 'AppBlog/usuario.html', {'form':form, 'titulo':'Iniciar sesión', 'submit':'Iniciar sesión'})


@login_required
def perfilUsario(request):
    usuario = request.user
    perfil = usuario.userprofile

    if request.method == 'POST':
        formulario = FormEditarPerfil(request.POST, request.FILES)
        if formulario.is_valid():
            info = formulario.cleaned_data
            if info['avatar']:
                perfil.avatar = info['avatar']
            else:
                perfil.avatar = 'avatares/avatardefault.png'
            perfil.biografia = info['biografia']
            perfil.save()
            return render(request, 'AppBlog/inicio.html')
    else:
        formulario = FormEditarPerfil(initial={'avatar':perfil.avatar, 'biografia':perfil.biografia})
    contexto = {'form':formulario, 'titulo':'Mi perfil', 'submit':'Guardar'}
    return render(request, 'AppBlog/perfil.html', contexto)


@login_required
def editarUsuario(request):
    usuarioConectado = request.user
    if request.method == 'POST':
        formulario = FormEditarUsuario(request.POST)
        if formulario.is_valid():
            info = formulario.cleaned_data
            usuarioConectado.email = info['email']
            usuarioConectado.first_name = info['first_name']
            usuarioConectado.last_name = info['last_name']
            usuarioConectado.password1 = info['password1']
            usuarioConectado.password2 = info['password2']
            usuarioConectado.save()
            return render(request, 'AppBlog/inicio.html')
    else:
        formulario = FormEditarUsuario(initial={'email':usuarioConectado.email, 'first_name':usuarioConectado.first_name, 'last_name':usuarioConectado.last_name})
    contexto = {'form':formulario, 'usuario':usuarioConectado, 'titulo':'Editar usuario', 'submit':'Guardar'}
    return render(request, 'AppBlog/usuario.html', contexto)


def listarCategorias(request):

    categs = Categoria.objects.all()

    return render(request, 'AppBlog/listadoCategoria.html', {'categs':categs,'titulo':f'Categorías'})


def buscarCateg(request):
    return render(request,'AppBlog/buscarCateg.html')


def buscarCategoria(request):

    if request.GET['nombre']:

        busqueda = request.GET["nombre"]
        categs = Categoria.objects.filter(nombre__icontains=busqueda)

        return render(request, 'AppBlog/listadoCategoria.html', {'categs':categs,'titulo':f'Resultado de la busqueda: {busqueda}'})

    else:
        
        mensaje = 'No enviaste datos'

    return HttpResponse(mensaje)


def crearCategoria(request):

    if request.method=='POST':

        form = FormularioCategoria(request.POST)

        if form.is_valid():

            info = form.cleaned_data

            categ = Categoria(nombre=info['nombre'])

            categ.save()

            return render(request, 'AppBlog/inicio.html')
    
    else:
        form = FormularioCategoria()
    
    return render(request, 'AppBlog/formCategoria.html', {'form':form})


class PublicacionLista(ListView):
    model = Publicacion


class PublicacionCrear(CreateView):
    model = Publicacion
    success_url = '/AppBlog/'
    fields = ['titulo','cuerpo','imagen','fecha'] #ver de que se creen con la fecha y hora de ahora


class MensajeCrear(CreateView): #solo para la primera entrega
    model = Mensaje
    success_url = '/AppBlog/'
    fields = ['remitente','destinatario','mensaje']