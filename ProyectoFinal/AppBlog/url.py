from django.urls import path
from django.contrib.auth.views import LogoutView
from AppBlog.views import *


urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro', registroUsuario, name='registro'),
    path('login', iniciarSesion, name='login'),
    path('perfilUsuario', perfilUsario, name='perfilUsuario'),
    path('editarUsuario', editarUsuario, name='editarUsuario'),
    path('logout', LogoutView.as_view(template_name='AppBlog/inicio.html'), name = 'logout'),
    path('categorias/', listarCategorias, name='listarCategorias'),
    path('crearCategoria/', crearCategoria, name='crearCategoria'),
    path('buscarCategoria/', buscarCateg, name='buscarCategoria'),
    path('buscar/', buscarCategoria),
    path('publicaciones/', PublicacionLista.as_view()),
    path('publicaciones/nueva', PublicacionCrear.as_view(), name='crearPublicacion'),
    path('mensaje/nuevo', MensajeCrear.as_view()),
]