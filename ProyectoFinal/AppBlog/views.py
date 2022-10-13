from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from AppBlog.models import *
from AppBlog.forms import *

def inicio(request):
    entradas = EntradaBlog.objects.all().order_by('-fecha')[:10]
    return render(request, 'AppBlog/inicio.html', {'entradas':entradas, 'titulo':'Bienvendio al blog'})


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
                return redirect('inicio')
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
        form = FormCrearCategoria(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            categ = Categoria(nombre=info['nombre'])
            categ.save()
            return render(request, 'AppBlog/inicio.html')
    else:
        form = FormCrearCategoria()

    return render(request, 'AppBlog/formCategoria.html', {'form':form})


class CrearEntrada(LoginRequiredMixin, CreateView):
    model = EntradaBlog
    template_name = 'AppBlog/entradaBlog.html'
    fields = ['titulo', 'subtitulo','cuerpo','imagen','categoria']
    success_url = '/AppBlog/'
    login_url = 'login'

    def form_valid(self, form):
        form.save(commit=False)
        usuario = User.objects.get(username = self.request.user)
        form.instance.autor = usuario
        form.save()
        return redirect(self.success_url)


class EditarEntrada(LoginRequiredMixin, UpdateView):
    model = EntradaBlog
    template_name= 'AppBlog/entradaBlog.html'
    fields = ['titulo', 'subtitulo','cuerpo','imagen','categoria']
    success_url = '/AppBlog/'
    login_url = 'login'


class ListaEntrada(ListView):
    model = EntradaBlog
    template_name = 'AppBlog/publicacion_list.html'


def ultimasEntradas(request):
    entradas = EntradaBlog.objects.all().order_by('-fecha')[:10]
    return render(request, 'AppBlog/blog.html', {'entradas':entradas})

@login_required
def misEntradas(request):
    entradas = EntradaBlog.objects.filter(autor=request.user).order_by('-fecha')
    return render(request, 'AppBlog/listaEntradas.html', {'entradas':entradas})


class BorrarEntrada(LoginRequiredMixin, DeleteView):
    model = EntradaBlog
    success_url = reverse_lazy('misEntradas')
    login_url = 'login'

class LeerEntrada(DetailView):
    model = EntradaBlog