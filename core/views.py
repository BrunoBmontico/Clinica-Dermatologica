from django.shortcuts import render, get_object_or_404, redirect                    # REQUESTS PADROES DJANGO
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout                         # REQUERIMENTO DE LOGIN
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator, has_permission_decorator # PERMISSOES DOS USUAROS
from rolepermissions.roles import assign_role
from django.contrib import messages
from .models import *                                                               # MODELS
from phonenumbers import NumberParseException

# CADASTRAR USUARIO
def cadastrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'core/cadastro.html')
    else:
        Nome_Usuario = request.POST.get('Nome_Usuario')
        Sobrenome_Usuario = request.POST.get('Sobrenome_Usuario')
        Tel_Usuario = request.POST.get('Tel_Usuario')
        Email_Usuario = request.POST.get('Email_Usuario')
        Senha_Usuario = request.POST.get('Senha_Usuario')
        Data_nsc_Usuario = request.POST.get('Data_nsc_Usuario')
        Sexo_Usuario = request.POST.get('Sexo_Usuario')
        Cpf_Usuario = request.POST.get('Cpf_Usuario')
        Cep_Usuario = request.POST.get('Cep_Usuario')
        Endr_Usuario = request.POST.get('Endr_Usuario')
        Img_Usuario = request.FILES.get('Img_Usuario')

        if Nome_Usuario and Sobrenome_Usuario and Senha_Usuario and Data_nsc_Usuario and Sexo_Usuario and Email_Usuario and Cep_Usuario and Cpf_Usuario:
            usuario = Paciente.objects.filter(username=Email_Usuario).first()
            if usuario:
                message_error = 'ERRO: Email já registrado!'
                messages.warning(request, message_error)
                return redirect('/cadastro/')
            else:
                usuario = Paciente(
                    first_name=Nome_Usuario,
                    last_name=Sobrenome_Usuario,
                    Tel_Usuario=Tel_Usuario,
                    email=Email_Usuario,
                    username=Email_Usuario,
                    Data_nsc_Usuario=Data_nsc_Usuario,
                    Sexo_Usuario=Sexo_Usuario,
                    Cpf_Usuario=Cpf_Usuario,
                    Cep_Usuario=Cep_Usuario,
                    Endr_Usuario=Endr_Usuario,
                    Img_Usuario=Img_Usuario,
                )

                try:
                    Tel_valido = Paciente.validator.validar_tel(Tel_Usuario)
                except NumberParseException:
                    message_error = 'ERRO: Número de telefone inválido!'
                    messages.warning(request, message_error)
                    return redirect('/cadastro/')
        
                cpf_valido = Paciente.validator.validar_cpf(Cpf_Usuario)
                cep_valido = Paciente.validator.validar_cep(Cep_Usuario)
        
                if not cpf_valido or not cep_valido:
                    message_error = 'ERRO: CPF ou CEP inválidos!'
                    messages.warning(request, message_error)
                    return redirect('/cadastro/')

                usuario.set_password(Senha_Usuario)
                usuario.save()
                assign_role(usuario, 'paciente')
                return redirect('/login/')
        else:
            message_error = 'ERRO: preencha todos os campos obrigatórios!'
            messages.warning(request, message_error)
            return redirect('/cadastro/')


# LOGAR USUARIO
def logar_usuario(request):
    if request.method == 'GET':
        return render(request, 'core/home_page.html')
    else:
        Email_Usuario = request.POST.get('Email_Usuario')
        Senha_Usuario = request.POST.get('Senha_Usuario')

        usuario = authenticate(username=Email_Usuario, password=Senha_Usuario)

        if usuario:
            login(request, usuario)
            if usuario.is_superuser:
                return redirect('/admin/')
            elif hasattr(usuario, 'paciente'):
                return redirect(f'/paciente/AreaConsulta/')
            elif hasattr(usuario, 'especialista'):
                return redirect('/medico/especialista_list/')
            else:
                return HttpResponse('Usuário sem papel definido.')
        else:
            return HttpResponse('Email ou senha inválidos')       

# PAGINA DE REDIRECIONAMENTO
def pagina_login(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')
    else:
        Email_Usuario = request.POST.get('Email_Usuario')
        Senha_Usuario = request.POST.get('Senha_Usuario')

        usuario = authenticate(username=Email_Usuario, password=Senha_Usuario)

        if usuario:
            login(request, usuario)
            if usuario.is_superuser:
                return redirect('/admin/')
            elif hasattr(usuario, 'paciente'):
                return redirect(f'/paciente/perfil_usuario/{request.user.id}')
            elif hasattr(usuario, 'especialista'):
                return redirect('/medico/especialista_list/')
            else:
                return HttpResponse('Usuário sem papel definido.')
        else:
            message_error = 'ERRO: Email ou senha inválidos'
            messages.warning(request, message_error)
            return redirect('/login/')

#LOGOUT USUARIO
@login_required(login_url='/login/')
def logout_usuario(request):
    logout(request)
    return redirect('/')

# AGENDAMENTO DE CONSULTA
@login_required(login_url='/login/')
def agendar_consulta(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    especialistas = Especialista.objects.all()

    if request.method == 'GET':
        return render(request, 'core/agendamento.html', {'especialistas': especialistas})
    else:
        medico = request.POST.get('especialista')
        especialidade = request.POST.get('especialidade')
        data = request.POST.get('data')

        for especialista in especialistas:
            if especialista.first_name and especialista.last_name in medico:

                if data != '' and medico != 'Qual profissional deseja escolher?' and especialidade != 'Qual procedimento deseja escolher?':
                    consulta = Consulta.objects.create(
                        Id_Usuario = usuario,
                        Id_Medico = especialista,
                        Medico = medico,
                        Especialidade = especialidade,
                        Data = data,
                    )
                consulta.save()
                return redirect('/paciente/AreaConsulta/')
        else:
            message_error = 'ERRO: Preencha todos os campos!'
            messages.warning(request, message_error)
            return redirect(f'/paciente/agendamento/{request.user.id}')