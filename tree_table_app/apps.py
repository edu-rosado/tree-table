from django.apps import AppConfig


class TreeTableAppConfig(AppConfig):
    name = 'tree_table_app'

    def ready(self):
        import tree_table_app.signals
