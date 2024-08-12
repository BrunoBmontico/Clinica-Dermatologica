from rolepermissions.decorators import has_role_decorator, has_permission_decorator # PERMISSOES DOS USUAROS
from rolepermissions.roles import assign_role
from django.shortcuts import render, get_object_or_404, redirect                    # REQUESTS PADROES DJANGO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required                           # REQUERIMENTO DE LOGIN
from core.models import Paciente, Consulta                                          # MODELS
from django.contrib import messages
from phonenumbers import NumberParseException


# AREA DO PACIENTE
@has_role_decorator('paciente')
@login_required(login_url='/login/')
def AreaPaciente(request):
    consultas = Consulta.objects.all()
    consultas_paciente = consultas.filter(Id_Usuario=request.user.id, Status='R')
    return render(request, 'paciente/resultado_exames.html', {'consultas_paciente': consultas_paciente})

# AREA DE CONSULTAS
@has_role_decorator('paciente')
@login_required(login_url='/login/')
def AreaConsulta(request):
    consultas = Consulta.objects.all()
    consultas_paciente = consultas.filter(Id_Usuario=request.user.id, Status='A')

    return render(request, 'paciente/area_consulta.html', {'consultas_paciente': consultas_paciente})

def cancelar_consulta(request, id):
    consulta = Consulta.objects.get(pk=id, Status='A')

    consulta.Status = 'C'
    consulta.save()
    return redirect('/paciente/AreaConsulta/')

#AREA LOCAL
@has_role_decorator('paciente')
@login_required(login_url='/login/')
def AreaLocal(request):
    return render(request, 'paciente/area_local.html')

# PREFIL DO USUARIO
@has_role_decorator('paciente')
@login_required(login_url='/login/')
def view_usuario(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    return render(request, 'paciente/perfil_usuario.html')

# EDITAR DADOS DO USUARIO
def Editar_dados(request, id):
    paciente = get_object_or_404(Paciente, pk=id)

    if request.method == 'GET':
        return render(request, 'core/perfil_usuario.html', {'user': paciente})
    else:
        new_img = request.FILES.get('img_perfilUsuario')
        edit_Nome = request.POST.get('Nome_Usuario')
        edit_Sobrenome = request.POST.get('Sobrenome_Usuario')
        edit_Telelfone = request.POST.get('Telefone_Usuario')
        edit_Email = request.POST.get('Email_Usuario')
        edit_CEP = request.POST.get('CEP_Usuario')
        edit_Endereco = request.POST.get('Endereco_Usuario')

        if edit_Nome and edit_Sobrenome and edit_Email and edit_Endereco:
            if new_img:
                paciente.Img_Usuario = new_img

            paciente.first_name = edit_Nome
            paciente.last_name = edit_Sobrenome
            paciente.Tel_Usuario = edit_Telelfone
            paciente.email = edit_Email
            paciente.username = edit_Email
            paciente.Cep_Usuario = edit_CEP
            paciente.Endr_Usuario = edit_Endereco

            try:
                Tel_valido = Paciente.validator.validar_tel(edit_Telelfone)
            except NumberParseException:
                message_error = 'ERRO: Número de telefone inválido!'
                messages.warning(request, message_error)
                return redirect(f'/paciente/perfil_usuario/{request.user.id}')
            
            cep_valido = Paciente.validator.validar_cep(edit_CEP)
            if not cep_valido:
                message_error = 'ERRO: CEP inválido!'
                messages.warning(request, message_error)
                return redirect(f'/paciente/perfil_usuario/{request.user.id}')

            paciente.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect(f'/paciente/perfil_usuario/{request.user.id}')
        else:
            message_error = 'ERRO: Preencha todos os campos obrigatórios!'
            messages.warning(request, message_error)
            return redirect(f'/paciente/perfil_usuario/{request.user.id}')

# EDITAR SENHA DO USUARIO
@login_required(login_url='/login/')
def editar_senha(request, id):
    paciente = get_object_or_404(Paciente, pk=id)

    if request.method == 'GET':
        return render(request, 'core/editar_senha.html')
    else:
        edit_SenhaAntg = request.POST.get('Senha_Antiga_Usuario')
        edit_Password = request.POST.get('Password')
        edit_Conf_Password = request.POST.get('Password_Confirm')

        if paciente.check_password(edit_SenhaAntg):
            if edit_Password == edit_Conf_Password and edit_Password != '':
                paciente.set_password(edit_Conf_Password)
                paciente.save()
                return redirect('/login/')
            else:
                message_error = 'ERRO: Senhas nao coincídem!'
                messages.warning(request, message_error)
                return redirect(f'/paciente/editar_senha/{request.user.id}')
        else:
            message_error = 'ERRO: Senha incorreta!'
            messages.warning(request, message_error)
            return redirect(f'/paciente/editar_senha/{request.user.id}')

def view_exames(request, id):
    consulta = get_object_or_404(Consulta, pk=id)

    return render(request, 'paciente/view_exames.html', {'consulta': consulta})

    # return HttpResponse(consulta)