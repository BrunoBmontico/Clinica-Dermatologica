from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

class PacienteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paciente'

class MedicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medico'