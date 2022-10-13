from django.urls import path
from django.contrib.auth.views import LogoutView
from AppBlog.views import *


urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro', registroUsuario, name='registro'),
    path('login', iniciarSesion, name='login'),
    path('perfilUsuario', perfilUsario, name='perfilUsuario'),
    path('editarUsuario', editarUsuario, name='editarUsuario'),
    path('logout', LogoutView.as_view(template_name='AppBlog/logout.html'), name = 'logout'),
    path('categorias/', listarCategorias, name='listarCategorias'),
    path('crearCategoria/', crearCategoria, name='crearCategoria'),
    path('buscarCategoria/', buscarCateg, name='buscarCategoria'),
    path('buscar/', buscarCategoria),
    path('crearEntrada/', CrearEntrada.as_view(), name='crearEntrada'),
    path('editarEntrada/<int:pk>', EditarEntrada.as_view(), name='editarEntrada'),
    path('misEntradas', misEntradas, name='misEntradas'),
    path('borrarEntrada/<int:pk>', BorrarEntrada.as_view(), name='borrarEntrada'),
    path('listaEntradas', ListaEntrada.as_view()),
    path('blog', ultimasEntradas),
    path('leerEntrada/<int:pk>', LeerEntrada.as_view(), name='leerEntrada'),
]