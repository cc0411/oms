from django.apps import AppConfig


class SaltConfig(AppConfig):
    name = 'salt'
    def ready(self):
        import salt.signals