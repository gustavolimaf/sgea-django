# 📚 Sistema de Gestão de Eventos Acadêmicos (SGEA)# sgea-django

Sistema de Gestão de Eventos Acadêmicos (SGEA) com Python e Django

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema web completo para gerenciamento de eventos acadêmicos como seminários, palestras, minicursos e semanas acadêmicas. Desenvolvido com Django, SQLite e seguindo as melhores práticas de desenvolvimento web.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso](#uso)
- [Documentação](#documentação)

## 🎯 Sobre o Projeto

O SGEA é uma plataforma web que facilita a organização, divulgação e gestão de eventos acadêmicos. O sistema permite que organizadores criem e gerenciem eventos, enquanto alunos e professores podem se inscrever facilmente e receber certificados digitais.

### Perfis de Usuário

- **Alunos**: Podem se inscrever em eventos e baixar certificados
- **Professores**: Podem se inscrever em eventos e baixar certificados
- **Organizadores**: Podem criar eventos, gerenciar inscrições e emitir certificados

## ✨ Funcionalidades

### 🔐 Autenticação e Cadastro

- ✅ Cadastro de novos usuários com validação de dados
- ✅ Login e logout seguros
- ✅ Perfis diferenciados (Aluno, Professor, Organizador)
- ✅ Gerenciamento de sessões

### 📅 Gestão de Eventos

- ✅ Criação de eventos com informações completas
- ✅ Edição de eventos existentes
- ✅ Tipos de eventos: Seminário, Palestra, Minicurso, Semana Acadêmica
- ✅ Controle de vagas e disponibilidade
- ✅ Filtros e busca de eventos

### 📝 Inscrições

- ✅ Inscrição simplificada em eventos
- ✅ Cancelamento de inscrições
- ✅ Visualização de eventos inscritos
- ✅ Validação de vagas disponíveis
- ✅ Histórico de inscrições

### 🎓 Certificados

- ✅ Emissão de certificados para participantes
- ✅ Download de certificados em PDF
- ✅ Código de verificação único
- ✅ Gerenciamento de certificados emitidos

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação
- **Django 4.2+** - Framework web
- **SQLite** - Banco de dados
- **HTML5/CSS3** - Frontend
- **ReportLab/WeasyPrint** - Geração de PDFs

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/gustavolimaf/sgea-django.git
cd sgea-django
```

2. **Crie um ambiente virtual**

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário**

```bash
python manage.py createsuperuser
```

6. **Execute o servidor**

```bash
python manage.py runserver
```

7. **Acesse o sistema**

- Sistema: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📖 Uso

### Para Alunos/Professores

1. Faça cadastro informando seu perfil e instituição
2. Navegue pelos eventos disponíveis
3. Inscreva-se nos eventos de interesse
4. Acompanhe suas inscrições no dashboard
5. Baixe certificados após conclusão dos eventos

### Para Organizadores

1. Acesse o painel de criação de eventos
2. Preencha informações do evento (tipo, data, local, vagas)
3. Gerencie inscrições e lista de participantes
4. Emita certificados para os participantes

### Para Administradores

- Acesse /admin com credenciais de superusuário
- Gerencie usuários, eventos, inscrições e certificados
- Visualize estatísticas e relatórios do sistema

## 📚 Documentação

### Modelos de Dados

- **Usuario**: Informações de usuários com perfis diferenciados
- **Evento**: Dados completos de eventos acadêmicos
- **Inscricao**: Relacionamento entre usuários e eventos
- **Certificado**: Certificados digitais com código de verificação

### Segurança

- Senhas com hash PBKDF2 SHA256
- Proteção CSRF em formulários
- Validação de dados de entrada
- Controle de permissões por perfil

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga o padrão PEP 8 e inclua testes para novas funcionalidades.

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Autor

**Gustavo Lima** - [@gustavolimaf](https://github.com/gustavolimaf)

---

**Desenvolvido com ❤️ usando Django**
