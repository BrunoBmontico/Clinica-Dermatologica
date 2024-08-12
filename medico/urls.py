from django.urls import path
from . import views
from .views import EspecialistaListView, ConsultaListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('cadastro_especialista/', views.cadastrar_especialista, name='cadastrar_especialista'),
    # path('especialista_list/<int:id>/', EspecialistaListView.as_view(), name='especialista'),
    path('especialista_list/', views.EspecialistaListView, name='especialista'),
    path('consulta_list/<int:pk>/', ConsultaListView.as_view(), name='consulta_list'),
    path('salvar_prontuario/<int:consulta_id>/', views.salvar_prontuario, name='salvar_prontuario'),
    path('salvar_receituario/<int:consulta_id>/', views.salvar_receituario, name='salvar_receituario'),
    path('cancelar_agendamento/<int:pk>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('finalizar_consulta/<int:pk>/', views.finalizar_consulta, name='finalizar_consulta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)