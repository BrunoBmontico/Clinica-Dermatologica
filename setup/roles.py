from rolepermissions.roles import AbstractUserRole

class Paciente(AbstractUserRole):
    available_permissions = {'acessar_areaPaciente': True}

class Especialista(AbstractUserRole):
    available_permissions = {'acessar_areaEspecialista': True}