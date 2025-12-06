#  Sistema de Gestão de Eventos Acadêmicos (SGEA)

Sistema de Gestão de Eventos Acadêmicos (SGEA) com Python e Django

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

##  Documentação do Projeto

- **[Requisitos e Casos de Uso](docs/REQUISITOS_E_CASOS_DE_USO.md)** - Documentação completa dos requisitos funcionais e casos de uso
- **[Diagrama Lógico do Banco de Dados](docs/diagrama_logico.md)** - Modelagem e estrutura do banco de dados

---

Sistema web completo para gerenciamento de eventos acadêmicos como seminários, palestras, minicursos e semanas acadêmicas. Desenvolvido com Django, SQLite e seguindo as melhores práticas de desenvolvimento web.

##  Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso](#uso)
- [Documentação](#documentação)

##  Sobre o Projeto

O SGEA é uma plataforma web que facilita a organização, divulgação e gestão de eventos acadêmicos. O sistema permite que organizadores criem e gerenciem eventos, enquanto alunos e professores podem se inscrever facilmente e receber certificados digitais.

### Perfis de Usuário

- **Alunos**: Podem se inscrever em eventos e baixar certificados
- **Professores**: Podem se inscrever em eventos e baixar certificados
- **Organizadores**: Podem criar eventos, gerenciar inscrições e emitir certificados

##  Funcionalidades

###  Autenticação e Cadastro

-  Cadastro com validação avançada (senha forte obrigatória)
-  Confirmação de email com token
-  Login e logout seguros
-  Perfis diferenciados (Aluno, Professor, Organizador)
-  Máscara de telefone: (XX) XXXXX-XXXX

###  Gestão de Eventos

-  CRUD completo de eventos (apenas organizadores)
-  Upload de banner com validação de imagem
-  Tipos: Seminário, Palestra, Minicurso, Semana Acadêmica
-  Professor responsável obrigatório
-  Controle de vagas e disponibilidade
-  Datas futuras obrigatórias
-  Filtros e busca de eventos

###  Inscrições

-  Inscrição em eventos com validação de vagas
-  Bloqueio automático quando lotado
-  Prevenção de inscrições duplicadas
-  Organizadores não podem se inscrever
-  Cancelamento de inscrições
-  Histórico completo

###  Certificados

-  Geração automática após término do evento
-  Download em PDF com QR Code
-  Código de verificação único
-  Validação de certificados

###  API REST

-  Autenticação por Token
-  Consulta de eventos (20 req/dia)
-  Inscrição em eventos (50 req/dia)
-  Throttling configurado

###  Auditoria

-  Registro de ações críticas
-  Consulta por data ou usuário
-  Interface para organizadores

###  Notificações

-  Email de boas-vindas automático
-  Confirmação de inscrições
-  Link de confirmação de cadastro

##  Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação
- **Django 4.2.7** - Framework web
- **Django REST Framework 3.14.0** - API REST
- **SQLite** - Banco de dados
- **HTML5/CSS3** - Frontend modular e responsivo
- **ReportLab** - Geração de certificados em PDF

### Arquitetura CSS

CSS modular com identidade visual padronizada:

- **base.css** - Estilos globais e variáveis CSS (cores, fontes)
- **home.css** - Página inicial
- **dashboard.css** - Dashboards de usuários
- **evento-inscritos.css** - Gerenciamento de inscritos
- **certificado.css** - Layout para PDFs

##  Instalação

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
python manage.py migrate
```

5. **Popule o banco com dados iniciais**

```bash
python seed_data.py
```

Isso criará 3 usuários de teste:
- **Organizador:** organizador@sgea.com / Admin@123
- **Professor:** professor@sgea.com / Professor@123
- **Aluno:** aluno@sgea.com / Aluno@123

6. **(Opcional) Crie um superusuário para acessar /admin**

```bash
python criar_superuser.py
```

Credenciais: admin / admin123

7. **Execute o servidor**

```bash
python manage.py runserver
```

8. **Acesse o sistema**

- Sistema: http://localhost:8000
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api

##  Uso

### Credenciais de Teste

Após executar `python seed_data.py`:

| Perfil | Login | Senha |
|--------|-------|-------|
| Organizador | organizador@sgea.com | Admin@123 |
| Professor | professor@sgea.com | Professor@123 |
| Aluno | aluno@sgea.com | Aluno@123 |
| Admin (opcional) | admin | admin123 |

### Para Alunos/Professores

1. Faça cadastro ou use credenciais de teste
2. Confirme email via link (tokens de teste já confirmados)
3. Navegue e filtre eventos disponíveis
4. Inscreva-se nos eventos (vagas limitadas)
5. Acompanhe inscrições no dashboard
6. Baixe certificados após término dos eventos

### Para Organizadores

1. Crie eventos com banner, datas e professor responsável
2. Gerencie inscritos e visualize estatísticas
3. Consulte logs de auditoria
4. Certificados são gerados automaticamente

### API REST

1. Obtenha token: `POST /api/token/` com username e password
2. Consulte eventos: `GET /api/eventos/` (20 req/dia)
3. Inscreva-se: `POST /api/inscricoes/` (50 req/dia)
4. Use header: `Authorization: Token seu_token`

##  Documentação

### Modelos de Dados

- **Usuario**: Usuários com perfis (Aluno, Professor, Organizador) e confirmação de email
- **Evento**: Eventos com banner, professor responsável, vagas e datas
- **Inscricao**: Inscrições com validação de duplicidade e vagas
- **Certificado**: Certificados com código único de verificação
- **Auditoria**: Registro de ações críticas do sistema

### Regras de Negócio

1. **Senha forte:** 8+ caracteres, letras, números e especiais
2. **Datas futuras:** Eventos só podem ser criados com data futura
3. **Professor obrigatório:** Todo evento deve ter professor responsável
4. **Bloqueio de vagas:** Inscrições bloqueadas quando lotado
5. **Sem duplicatas:** Usuário não pode se inscrever duas vezes
6. **Organizadores:** Não podem se inscrever em eventos

### Segurança

- Senhas com hash PBKDF2 SHA256
- Proteção CSRF em formulários
- Validação avançada de entrada (telefone, email, imagens)
- Controle de permissões por perfil
- Token de confirmação de email
- Throttling na API (20/50 req/dia)

##  Contribuindo

Contribuições são bem-vindas! Siga o padrão PEP 8 e inclua testes para novas funcionalidades.

##  Licença

Este projeto está sob a licença MIT.

##  Autores

**Gustavo Lima** - [@gustavolimaf](https://github.com/gustavolimaf)

**Lucas Villas** - [@Lucasvillas](https://github.com/Lucasvillas)

**Sabrina Vianna** - [@littlesabs](https://github.com/LittleSabs)
