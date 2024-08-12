from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import *
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
import pytz

# FORMULARIO DO ESPECIALISTA
class EspecialistaCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Especialista
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email', 'Tel_Usuario', 'Data_nsc_Usuario', 'Sexo_Usuario', 'Cpf_Usuario',
            'Cep_Usuario', 'Endr_Usuario', 'crm', 'especialidade', 'salario', 'Img_Usuario'
        )

# CADASTRAR ESPECIALISTA        
@login_required(login_url='/login/')
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def cadastrar_especialista(request):
    if not request.user.is_staff:
        messages.error(request, "Você não tem permissão para criar um especialista.")
        return redirect('/login/')
    
    if request.method == 'GET':
        form = EspecialistaCreationForm()
        return render(request, 'core/cadastro_especialista.html', {'form': form})
    else:
        form = EspecialistaCreationForm(request.POST, request.FILES)  # Add request.FILES to handle file uploads
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_especialista = True
            usuario.save()
            return redirect('/')
        else:
            return render(request, 'core/cadastro_especialista.html', {'form': form})

# AREA PRINCIPAL DO ESPECIALISTA
# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class EspecialistaListView(TemplateView):
#     template_name = 'medico/especialista_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Obtendo o especialista
#         especialista = self.request.user

#         # Define o fuso horário desejado (America/Sao_Paulo para o Brasil)
#         fuso_horario_brasileiro = pytz.timezone('America/Sao_Paulo')

#         # Obtendo a data atual no fuso horário brasileiro
#         data_atual_brasileira = timezone.now().astimezone(fuso_horario_brasileiro).date()

#         # Definindo a saudação com base no sexo
#         if hasattr(especialista, 'sexo'):
#             saudacao = "Bem vinda, Dra." if especialista.sexo == "F" else "Bem vindo, Dr."
#         else:
#             saudacao = "Bem vindo, Dr."  # Default caso o campo sexo não exista

#         # Consultas agendadas para o dia atual associadas ao especialista logado, ordenadas por hora
#         consultas = Consulta.objects.filter(Medico=especialista, Data__date=data_atual_brasileira).order_by('Data')
#         consultas_agendadas = consultas.filter(Status='A')
#         consultas_espera = consultas.filter(Status='E')
#         num_agendadas = consultas_agendadas.count()
#         num_esperas = consultas_espera.count()

#         # Verificar e atualizar status das consultas
#         for consulta in consultas_agendadas:
#             if consulta.Data < timezone.now():
#                 consulta.Status = 'C'  # Consulta cancelada
#                 consulta.save()

#         # Adicionando dados ao contexto
#         context['saudacao'] = saudacao
#         context['especialista'] = especialista
#         context['data_atual'] = data_atual_brasileira.strftime('%d/%m/%Y')
#         context['num_agendadas'] = num_agendadas
#         context['num_esperas'] = num_esperas
#         context['consultas_agendadas'] = consultas_agendadas.exists()
#         context['consultas_espera'] = consultas_espera.exists()
#         context['consultas'] = consultas

#         return context
    
def EspecialistaListView(request):
    # Define o fuso horário desejado (America/Sao_Paulo para o Brasil)
    fuso_horario_brasileiro = pytz.timezone('America/Sao_Paulo')

    # Obtendo a data atual no fuso horário brasileiro
    data_atual_brasileira = timezone.now().astimezone(fuso_horario_brasileiro).date()

    # Consultas agendadas para o dia atual associadas ao especialista logado, ordenadas por hora
    from django.db.models import Q
    consultas = Consulta.objects.all()
    consultas_agendadas = consultas.filter(Id_Medico=request.user.id, Data__date=data_atual_brasileira).filter(Q(Status='A') | Q(Status='E')).order_by('Data')
    consultas_espera = consultas.filter(Id_Medico=request.user.id, Status='E')
        

    # Obtendo o especialista
    especialista = request.user

    if hasattr(especialista, 'sexo'):
        saudacao = "Bem vinda, Dra." if especialista.sexo == "F" else "Bem vindo, Dr."
    else:
        saudacao = "Bem vindo, Dr."  # Default caso o campo sexo não exista

    num_agendadas = consultas_agendadas.count()
    num_esperas = consultas_espera.count()

    # Verificar e atualizar status das consultas
    for consulta in consultas_agendadas:
        if consulta.Data < timezone.now():
            consulta.Status = 'C'  # Consulta cancelada
            consulta.save()

    context = {
        'consultas_espera': consultas_espera,
        'consultas_agendadas': consultas_agendadas,
        'saudacao': saudacao,
        'especialista': especialista,
        'data_atual': data_atual_brasileira.strftime('%d/%m/%Y'),
        'num_agendadas': num_agendadas,
        'num_esperas': num_esperas,
        'consultas': consultas,
    }

    return render(request, 'medico/especialista_list.html', context)

# LISTA DE CONSULTAS DO ESPECIALISTA
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConsultaListView(TemplateView):
    template_name = 'medico/consulta_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        consulta = get_object_or_404(Consulta, pk=pk)
        context['object'] = consulta
        context['paciente'] = consulta.Id_Usuario
        return context
      
    
# SALVAR PRONTUARIO
@login_required
def salvar_prontuario(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    if request.method == 'POST':
        prontuario = request.POST.get('prontuario')
        consulta.Prontuario = prontuario
        consulta.save()
        return redirect('consulta_list', pk=consulta.id)

# SALVAR RECEITA
@login_required
def salvar_receituario(request, consulta_id):
    consulta = get_object_or_404(Consulta, pk=consulta_id)
    if request.method == 'POST':
        receituario = request.POST.get('receituario')
        consulta.Receita = receituario
        consulta.save()
        return redirect('consulta_list', pk=consulta.pk)

# SALVAR EXAME
@login_required
def salvar_exame(request):
    if request.method == 'POST':
        consulta_id = request.POST.get('consulta_id')
        exame = request.POST.get('exame')
        consulta = Consulta.objects.get(pk=consulta_id)
        consulta.exame = exame
        consulta.save()
        return redirect('consulta_list', pk=consulta.pk)
    
# CANCELAR AGENDAMENTO
@login_required
def cancelar_agendamento(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.Medico == request.user.username
    consulta.Status = 'C'
    consulta.save()
    return redirect('/medico/especialista_list/')

# FINALIZAR CONSULTA
@login_required
def finalizar_consulta(request, pk):
    # Obtenha o objeto Consulta ou retorne um erro 404 se não for encontrado
    consulta = get_object_or_404(Consulta, pk=pk)
    
    consulta.Medico == request.user
    consulta.Status = 'R'
    consulta.save()
    return redirect('/medico/especialista_list/')