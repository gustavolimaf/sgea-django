"""
URLs para o Sistema de Gestão de Eventos Acadêmicos (SGEA)
"""
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Autenticação
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Eventos
    path('eventos/', views.eventos_list, name='eventos_list'),
    path('eventos/<int:pk>/', views.evento_detail, name='evento_detail'),
    path('eventos/novo/', views.evento_create, name='evento_create'),
    path('eventos/<int:pk>/editar/', views.evento_edit, name='evento_edit'),
    path('eventos/<int:pk>/inscritos/', views.evento_inscritos, name='evento_inscritos'),
    
    # Inscrições
    path('inscricoes/criar/<int:evento_pk>/', views.inscricao_create, name='inscricao_create'),
    path('inscricoes/<int:pk>/cancelar/', views.inscricao_cancelar, name='inscricao_cancelar'),
    path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),
    
    # Certificados
    path('certificados/', views.meus_certificados, name='meus_certificados'),
    path('certificados/<int:pk>/download/', views.certificado_download, name='certificado_download'),
    path('certificados/emitir/<int:inscricao_pk>/', views.certificado_emitir, name='certificado_emitir'),
]
