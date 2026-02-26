from typing import Any


from django.contrib import admin
from .models import Filme, Episodio, Usuario
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# Aqui só existe porque quero mostrar os filmes vistos pelo usuário na página de administração do Django, 
# para isso preciso criar um campo personalizado para isso, e para isso preciso herdar do UserAdmin, 
# que é a classe de administração do modelo de usuário padrão do Django, e adicionar o campo filmes_vistos na lista de campos que são exibidos na página de administração do usuário.  
campos = list( UserAdmin.fieldsets  )
campos.append(('Filmes vistos', {'fields': ['filmes_vistos'],}))
UserAdmin.fieldsets = tuple(campos)

admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin)