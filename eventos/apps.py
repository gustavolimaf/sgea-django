from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'
    verbose_name = 'Sistema de Gestão de Eventos Acadêmicos'
    
    def ready(self):
        """
        Importa os signals quando o app estiver pronto
        """
        import eventos.signals
