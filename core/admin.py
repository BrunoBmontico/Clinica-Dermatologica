from django.contrib import admin
from .models import *


admin.site.register(Paciente, RemoveFieldPaciente)
admin.site.register(Especialista, RemoveFieldStaff)
# admin.site.register(Consulta)
admin.site.register(Especialidade)

admin.site.site_header = "Clínica Pink Diamond"
admin.site.index_title = "Admistração Clínica Pink Diamond"

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('get_paciente_name', 'Data', 'Status', 'Medico', 'Especialidade')
    search_fields = ('Id_Usuario__first_name', 'Id_Usuario__last_name', 'Id_Medico__first_name', 'Id_Medico__last_name', 'Status')

    def get_paciente_name(self, obj):
        return f"{obj.Id_Usuario.first_name} {obj.Id_Usuario.last_name}"
    get_paciente_name.short_description = 'Nome do Paciente'

admin.site.register(Consulta, ConsultaAdmin)
