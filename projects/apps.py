from django.apps import AppConfig


class AssetsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        super(AssetsConfig, self).ready()
        from . import signals
