from operator import is_
from django.apps import AppConfig


class FilmeConfig(AppConfig):
    name = "filme"
    from .models import Usuario
    import os
    email = os.getenv('EMAIL_ADMIN')
    senha = os.getenv('SENHA_ADMIN')

    usuarios = Usuario.objects.filter(email=email)
    if not usuarios:
        Usuario.objects.create_superuser(email=email, password=senha, is_active=True,is_staff=True, is_superuser=True)
