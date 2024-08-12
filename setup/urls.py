from django.contrib import admin
from django.urls import path, include
from core import views
import medico.urls
import paciente.urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.logar_usuario, name='logar_usuario'),
    path('cadastro/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.pagina_login, name='pagina_login'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('agendamento/<int:id>', views.agendar_consulta, name='agendar_consulta'),
    
    path('medico/', include(medico.urls)),
    path('paciente/', include(paciente.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)