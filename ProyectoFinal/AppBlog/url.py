from django.urls import path
from AppBlog.views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('categorias/', listarCategorias, name='listarCategorias'),
    path('crearCategoria/', crearCategoria, name='crearCategoria'),
    path('buscarCategoria/', buscarCateg, name='buscarCategoria'),
    path('buscar/', buscarCategoria),
    path('publicaciones/', PublicacionLista.as_view()),
    path('publicaciones/nueva', PublicacionCrear.as_view()),
    path('mensaje/nuevo', MensajeCrear.as_view()),
]