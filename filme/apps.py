from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "filme"

    # Aqui estamos sobrescrevendo o método ready para criar um superusuário automaticamente 
    # quando a aplicação for iniciada. Ele verifica se já existe um usuário com o email definido
    # nas variáveis de ambiente, e se não existir, ele cria um superusuário com esse email e senha.
    def ready(self):
        from .models import Usuario
        import os
        email = os.getenv('EMAIL_ADMIN')
        senha = os.getenv('SENHA_ADMIN')

        usuarios = Usuario.objects.filter(email=email)
        if not usuarios:
            Usuario.objects.create_superuser(email=email, password=senha, is_active=True,is_staff=True, is_superuser=True)
