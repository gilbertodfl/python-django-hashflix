from django.apps import AppConfig


class FilmeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "filme"

    # Removemos a criação automática de superusuário do método ready()
    # para evitar acessar o banco durante a inicialização do app.
