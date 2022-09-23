from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from AppBlog.models import *
from AppBlog.forms import *

def inicio(request):
    return render(request, 'AppBlog/inicio.html')


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