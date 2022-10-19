from django.urls import path
from django.contrib.auth.views import LogoutView
from AppBlog.views import *


urlpatterns = [
    path('', inicio, name='inicio'),
    path('about', about, name='about'),
    path('registro', registroUsuario, name='registro'),
    path('login', iniciarSesion, name='login'),
    path('perfilUsuario', perfilUsario, name='perfilUsuario'),
    path('editarUsuario', editarUsuario, name='editarUsuario'),
    path('logout', LogoutView.as_view(template_name='AppBlog/logout.html'), name = 'logout'),
    path('categorias/', listarCategorias, name='categorias'),
    path('crearCategoria/', crearCategoria, name='crearCategoria'),
    path('buscarCategoria/', buscarCategoria, name='buscarCategoria'),
    path('borrarCategoria/<int:pk>', BorrarCategoria.as_view(), name='borrarCategoria'),
    path('crearEntrada/', CrearEntrada.as_view(), name='crearEntrada'),
    path('editarEntrada/<int:pk>', EditarEntrada.as_view(), name='editarEntrada'),
    path('todasLasEntradas', todasLasEntradas, name='todasLasEntradas'),
    path('misEntradas', misEntradas, name='misEntradas'),
    path('borrarEntrada/<int:pk>', BorrarEntrada.as_view(), name='borrarEntrada'),
    path('buscarEntrada/', buscarEntradas, name='buscarEntrada'),
    path('entradasPorCategoria/<int:id>', entradasPorCategoria, name='entradasPorCategoria'),
    path('leerEntrada/<int:pk>', LeerEntrada.as_view(), name='leerEntrada'),
]