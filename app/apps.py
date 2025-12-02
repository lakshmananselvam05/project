from django.apps import AppConfig # pyright: ignore[reportMissingModuleSource]


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
