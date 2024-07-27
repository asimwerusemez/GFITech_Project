from django.apps import AppConfig


class ObjectifConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'objectif'

    def ready(self):
        from objectif import signals
