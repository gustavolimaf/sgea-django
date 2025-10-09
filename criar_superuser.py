"""
Script para criar superusuário inicial
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgea.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Verificar se já existe
if User.objects.filter(username='admin').exists():
    print("❌ Superusuário 'admin' já existe!")
else:
    User.objects.create_superuser(
        username='admin',
        email='admin@sgea.com',
        password='admin123',
        first_name='Administrador',
        last_name='SGEA',
        perfil='ORGANIZADOR',
        telefone='+5511999999999'
    )
    print("✅ Superusuário criado com sucesso!")
    print("   Usuário: admin")
    print("   Senha: admin123")
