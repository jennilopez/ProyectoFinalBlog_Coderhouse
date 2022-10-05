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