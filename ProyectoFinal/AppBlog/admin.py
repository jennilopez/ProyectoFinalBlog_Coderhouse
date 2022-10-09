from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Categoria)
admin.site.register(Publicacion)
admin.site.register(Mensaje)