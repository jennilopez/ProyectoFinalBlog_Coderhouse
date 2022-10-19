from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.db.models import Q
from AppBlog.models import *
from AppBlog.forms import *


def inicio(request):
    entradas = EntradaBlog.objects.all().order_by('-fecha')[:10]
    categorias = Categoria.objects.all().order_by('-id')[:6]
    contexto = {'entradas':entradas, 'categorias':categorias, 'titulo':'Bienvenido al blog'}
    return render(request, 'AppBlog/inicio.html', contexto)


def about(request):
    return render(request, 'AppBlog/about.html')


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
            return redirect('inicio')
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
            return redirect('inicio')
    else:
        formulario = FormEditarUsuario(initial={'email':usuarioConectado.email, 'first_name':usuarioConectado.first_name, 'last_name':usuarioConectado.last_name})
    contexto = {'form':formulario, 'usuario':usuarioConectado, 'titulo':'Editar usuario', 'submit':'Guardar'}
    return render(request, 'AppBlog/usuario.html', contexto)


def listarCategorias(request):
    categs = Categoria.objects.all()
    return render(request, 'AppBlog/listadoCategoria.html', {'categs':categs,'titulo':'Categorías'})


def buscarCategoria(request):
    if request.GET.get('categoria',False):
        busqueda = request.GET['categoria']
        categorias = Categoria.objects.filter(nombre__icontains=busqueda)
        mensaje = ''
        if not categorias:
            mensaje = 'No hay resultados para esta búsqueda'
        return render(request, 'AppBlog/listadoCategoria.html', {'categs':categorias,'titulo':f'Resultado de la busqueda: {busqueda}', 'mensaje':mensaje})
    else:
        return redirect('inicio')


@staff_member_required
def crearCategoria(request):
    if request.method=='POST':
        form = FormCrearCategoria(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            categ = Categoria(nombre=info['nombre'])
            categ.save()
            return redirect('categorias')
    else:
        form = FormCrearCategoria()
    return render(request, 'AppBlog/formCategoria.html', {'form':form})

@method_decorator(staff_member_required, name='dispatch')
class BorrarCategoria(DeleteView):
    model = Categoria
    success_url = reverse_lazy('categorias')


class CrearEntrada(LoginRequiredMixin, CreateView):
    model = EntradaBlog
    template_name = 'AppBlog/entradaBlog.html'
    fields = ['titulo', 'subtitulo','cuerpo','imagen','categoria']
    success_url = '/AppBlog/misEntradas'
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


def todasLasEntradas(request):
    entradas = EntradaBlog.objects.all().order_by('-fecha')
    return render(request, 'AppBlog/listaEntradas.html', {'entradas':entradas, 'titulo':'Todas las entradas'})


@login_required
def misEntradas(request):
    entradas = EntradaBlog.objects.filter(autor=request.user).order_by('-fecha')
    return render(request, 'AppBlog/listaEntradas.html', {'entradas':entradas, 'titulo':'Mis entradas'})


def buscarEntradas(request):
    if request.GET.get('entrada',False):
        busqueda = request.GET["entrada"]
        entradas = EntradaBlog.objects.filter(Q(titulo__icontains=busqueda) | Q(subtitulo__icontains=busqueda) | Q(cuerpo__icontains=busqueda))
        return render(request, 'AppBlog/listaEntradas.html', {'entradas':entradas,'titulo':f'Resultado de la busqueda: {busqueda}'})
    else:
        return redirect('inicio')


def entradasPorCategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    entradas = EntradaBlog.objects.filter(categoria=id)
    mensaje = ''
    if not entradas:
        mensaje = 'No hay resultados para esta búsqueda'
    return render(request, 'AppBlog/listaEntradas.html', {'entradas':entradas, 'titulo':f'Resultado de la busqueda: {categoria}', 'mensaje':mensaje})


class BorrarEntrada(LoginRequiredMixin, DeleteView):
    model = EntradaBlog
    success_url = reverse_lazy('misEntradas')
    login_url = 'login'

class LeerEntrada(DetailView):
    model = EntradaBlog