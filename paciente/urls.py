from django.urls import path
from paciente import views


urlpatterns = [
    path('AreaPaciente/', views.AreaPaciente, name='AreaPaciente'),
    path('AreaConsulta/', views.AreaConsulta, name='AreaConsulta'),
    path('cancelar_consulta/<int:id>', views.cancelar_consulta, name='cancelar_consulta'),
    path('Editar_dados/<int:id>/', views.Editar_dados, name='Editar_dados'),
    path('editar_senha/<int:id>/', views.editar_senha, name='editar_senha'),
    path('AreaLocal/', views.AreaLocal),
    path('perfil_usuario/<int:id>/', views.view_usuario, name='view_usuario'),
    path('view_exames/<int:id>/', views.view_exames, name='view_exames'),
    
]