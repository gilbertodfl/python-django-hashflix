import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria automaticamente um superusuário usando EMAIL_ADMIN e SENHA_ADMIN."

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.getenv("EMAIL_ADMIN")
        senha = os.getenv("SENHA_ADMIN")

        if not email or not senha:
            self.stdout.write(
                self.style.WARNING(
                    "Variáveis de ambiente EMAIL_ADMIN e/ou SENHA_ADMIN não definidas. "
                    "Nenhum usuário foi criado."
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.SUCCESS(
                    f"Já existe um usuário com o email {email}. Nenhuma ação necessária."
                )
            )
            return

        User.objects.create_superuser(
            username="admin",
            email=email,
            password=senha,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Superusuário criado com sucesso com o email {email}.")
        )

