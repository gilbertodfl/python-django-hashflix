from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "filme"

    # Aqui estamos sobrescrevendo o método ready para criar um superusuário automaticamente 
    # quando a aplicação for iniciada. Ele verifica se já existe um usuário com o email definido
    # nas variáveis de ambiente, e se não existir, ele cria um superusuário com esse email e senha.
    def ready(self):
        import os
        from django.db.utils import ProgrammingError, OperationalError
        from .models import Usuario

        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")

        # Em ambiente recém-criado (como no deploy), as migrações ainda podem não ter sido
        # aplicadas, então a tabela filme_usuario pode não existir. Nesse caso, apenas saímos.
        try:
            if not email or not senha:
                return

            usuarios = Usuario.objects.filter(email=email)
            if not usuarios:
                Usuario.objects.create_superuser(
                    username="admin",
                    email=email,
                    password=senha,
                    is_active=True,
                    is_staff=True,
                    is_superuser=True,
                )
        except (ProgrammingError, OperationalError):
            # Tabela ainda não existe ou banco não está pronto (por exemplo, antes das migrações)
            return
