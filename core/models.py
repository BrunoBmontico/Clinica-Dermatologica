from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib import admin
from django.conf import settings
from validate_docbr import CPF
from django.db import models
from datetime import date
import phonenumbers
import requests
import re

class UsuarioValidator:
    def validar_cpf(self, cpf):
        cpf_validator = CPF()
        if cpf_validator.validate(cpf):
            return cpf
    
    def validar_cep(self, cep):
        cep_validator = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(cep_validator)
        data = response.json()

        if 'erro' in data:
            return False
        else:
            return True
        
    def validar_tel(self, tel):
        tel_validator = phonenumbers.parse(tel)
        if phonenumbers.is_valid_number(tel_validator):
            return True
        else:
            return False

class Usuario(AbstractUser):
    SEXO_CHOICES = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )

    validator = UsuarioValidator()

    Tel_Usuario = models.CharField(verbose_name='Telefone', max_length=14, blank=False, null=False)
    Data_nsc_Usuario = models.DateField(verbose_name='Data de Nascimento', max_length=999, blank=False, null=True)
    Sexo_Usuario = models.CharField(verbose_name='Sexo do Usuário', max_length=10, choices=SEXO_CHOICES, blank=False, null=False)
    Cpf_Usuario = models.CharField(verbose_name='CPF', max_length=11, blank=False, null=False)
    Cep_Usuario = models.CharField(verbose_name='CEP', max_length=8, blank=False, null=False)
    Endr_Usuario = models.CharField(verbose_name='Endereço', max_length=100, blank=False, null=False)
    Img_Usuario = models.ImageField(verbose_name='Imagem de Usuário', upload_to='', blank=True, null=True)
    
    def __str__(self):
        return self.first_name

class Paciente(Usuario):
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        

class RemoveFieldStaff(admin.ModelAdmin):
    fields = (
        'first_name','last_name',
        'username', 'email',
        'password', 'crm',
        'especialidade', 'Tel_Usuario',
        'Cpf_Usuario', 'Cep_Usuario',
        'Endr_Usuario', 'Sexo_Usuario',
        'salario',
        'Img_Usuario',
        )
    exclude = (
        'last_login', 'is_superuser',
        'date_joined','is_paciente'
        )

class RemoveFieldPaciente(admin.ModelAdmin):
    fields = (
        'first_name', 'last_name',
        'email', 'Tel_Usuario',
        'Cpf_Usuario', 'Cep_Usuario',
        'Endr_Usuario', 'Sexo_Usuario',
        'Img_Usuario',
        )
    exclude = (
        'last_login', 'username',
        'is_superuser', 'date_joined',
        'is_paciente', 'password'
        )

class Especialidade(models.Model):
    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"

    CHOICES = (
        ("Dermatologista", "Dermatologista"),
        ("Cirurgia", "Cirurgia"),
        ("Clínica Geral", "Clínica Geral"),
        ("Odontologia", "Odontologia"),
    )
    
    nome = models.CharField("Especialidade", max_length=50, choices=CHOICES, primary_key=True)
    descricao = models.TextField("Descricao", max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Especialista(Usuario):
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    salario = models.CharField(verbose_name="Salário", null=True, blank=True, max_length=10)
    crm = models.CharField(verbose_name="CRM", max_length=20, null=False, blank=False)
    especialidade = models.ForeignKey(Especialidade, verbose_name="Especialidade", on_delete=models.CASCADE, null=True, blank=True)
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "especialidade"]
    is_especialista = models.BooleanField(default=True)
    def __str__(self):
        return self.first_name

class Consulta(models.Model):
    STATUS_CHOICES = (
        ('A', 'Agendada'),
        ('C', 'Cancelada'),
        ('E', 'Espera'),
        ('R', 'Realizada'),
    )

    Id_Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True, related_name='id_usuario')
    Id_Medico = models.ForeignKey(Especialista, on_delete=models.CASCADE, blank=True, null=True, related_name='id_medico')
    Medico = models.CharField(max_length=999, blank=True, null=True)
    Especialidade = models.CharField(max_length=999, blank=True, null=True)
    Data = models.DateTimeField(max_length=999, blank=False, null=False)
    Status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=False, null=False, default='A')
    Prontuario = models.TextField(blank=True, null=True)
    Exame = models.TextField(blank=True, null=True)
    Receita = models.TextField(blank=True, null=True)

    def __str__(self):
        return f" {self.Prontuario} {self.Receita}"
