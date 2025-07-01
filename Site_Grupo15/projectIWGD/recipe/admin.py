from django.contrib import admin
from .models import Receita, Ingrediente, Perfil, Comentario, Classificacao

# Modelos a serem geridos pelo Admin
admin.site.register(Receita)
admin.site.register(Ingrediente)
admin.site.register(Perfil)
admin.site.register(Comentario)
admin.site.register(Classificacao)
