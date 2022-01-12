from django.apps import AppConfig


class LocalhostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'localhost'
    verbose_name = 'Контейнер корпоративных паролей'