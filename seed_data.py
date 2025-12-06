"""
Script de seeding para popular o banco de dados com dados iniciais
Conforme especificação do projeto_2.md

Executar com: python manage.py shell < seed_data.py
Ou: python seed_data.py
"""
import os
import django
from datetime import date, time, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgea.settings')
django.setup()

from django.utils import timezone
from eventos.models import Usuario, Evento


def criar_usuarios():
    """
    Cria os usuários de teste conforme especificação
    """
    usuarios = []
    
    # Organizador
    if not Usuario.objects.filter(username='organizador@sgea.com').exists():
        org = Usuario.objects.create_user(
            username='organizador@sgea.com',
            email='organizador@sgea.com',
            password='Admin@123',
            first_name='João',
            last_name='Organizador',
            telefone='(11) 91234-5678',
            perfil='ORGANIZADOR',
            email_confirmado=True
        )
        usuarios.append(org)
        print(f' Organizador criado: {org.username}')
    
    # Professor
    if not Usuario.objects.filter(username='professor@sgea.com').exists():
        prof = Usuario.objects.create_user(
            username='professor@sgea.com',
            email='professor@sgea.com',
            password='Professor@123',
            first_name='Maria',
            last_name='Silva',
            telefone='(11) 92345-6789',
            instituicao='Universidade Federal',
            perfil='PROFESSOR',
            email_confirmado=True
        )
        usuarios.append(prof)
        print(f' Professor criado: {prof.username}')
    
    # Aluno
    if not Usuario.objects.filter(username='aluno@sgea.com').exists():
        aluno = Usuario.objects.create_user(
            username='aluno@sgea.com',
            email='aluno@sgea.com',
            password='Aluno@123',
            first_name='Pedro',
            last_name='Santos',
            telefone='(11) 93456-7890',
            instituicao='Universidade Federal',
            perfil='ALUNO',
            email_confirmado=True
        )
        usuarios.append(aluno)
        print(f' Aluno criado: {aluno.username}')
    
    return usuarios


def criar_eventos_exemplo():
    """
    Cria alguns eventos de exemplo para demonstração
    """
    try:
        organizador = Usuario.objects.get(username='organizador@sgea.com')
        professor = Usuario.objects.get(username='professor@sgea.com')
    except Usuario.DoesNotExist:
        print(' Erro: Usuários não encontrados. Execute criar_usuarios() primeiro.')
        return
    
    eventos = []
    hoje = date.today()
    
    # Evento 1: Workshop de Python
    if not Evento.objects.filter(nome='Workshop de Python para Iniciantes').exists():
        evento1 = Evento.objects.create(
            tipo='MINICURSO',
            nome='Workshop de Python para Iniciantes',
            descricao='Aprenda os fundamentos da programação Python com exemplos práticos.',
            data_inicial=hoje + timedelta(days=7),
            data_final=hoje + timedelta(days=7),
            horario_inicio=time(14, 0),
            horario_fim=time(18, 0),
            local='Laboratório de Informática - Bloco 2',
            vagas_totais=30,
            organizador=organizador,
            professor_responsavel=professor,
            ativo=True
        )
        eventos.append(evento1)
        print(f' Evento criado: {evento1.nome}')
    
    # Evento 2: Semana de Tecnologia
    if not Evento.objects.filter(nome='Semana de Tecnologia e Inovação').exists():
        evento2 = Evento.objects.create(
            tipo='SEMANA_ACADEMICA',
            nome='Semana de Tecnologia e Inovação',
            descricao='Uma semana completa de palestras, workshops e networking sobre tecnologia.',
            data_inicial=hoje + timedelta(days=15),
            data_final=hoje + timedelta(days=19),
            horario_inicio=time(8, 0),
            horario_fim=time(17, 0),
            local='Auditório Principal',
            vagas_totais=200,
            organizador=organizador,
            professor_responsavel=professor,
            ativo=True
        )
        eventos.append(evento2)
        print(f' Evento criado: {evento2.nome}')
    
    # Evento 3: Palestra sobre IA
    if not Evento.objects.filter(nome='Inteligência Artificial na Prática').exists():
        evento3 = Evento.objects.create(
            tipo='PALESTRA',
            nome='Inteligência Artificial na Prática',
            descricao='Descubra como a IA está transformando o mundo e suas aplicações práticas.',
            data_inicial=hoje + timedelta(days=30),
            data_final=hoje + timedelta(days=30),
            horario_inicio=time(19, 0),
            horario_fim=time(21, 0),
            local='Auditório Bloco B',
            vagas_totais=100,
            organizador=organizador,
            professor_responsavel=professor,
            ativo=True
        )
        eventos.append(evento3)
        print(f' Evento criado: {evento3.nome}')
    
    return eventos


def main():
    """
    Função principal para executar o seeding
    """
    print('\n' + '='*60)
    print('SGEA - Script de Seeding de Dados Iniciais')
    print('='*60 + '\n')
    
    print('Criando usuários de teste...')
    usuarios = criar_usuarios()
    
    print('\nCriando eventos de exemplo...')
    eventos = criar_eventos_exemplo()
    
    print('\n' + '='*60)
    print('Seeding concluído!')
    print('='*60)
    print('\nUsuários criados:')
    print('  - organizador@sgea.com / Admin@123')
    print('  - professor@sgea.com / Professor@123')
    print('  - aluno@sgea.com / Aluno@123')
    print('\nVocê pode fazer login com esses usuários no sistema.')
    print('='*60 + '\n')


if __name__ == '__main__':
    main()
