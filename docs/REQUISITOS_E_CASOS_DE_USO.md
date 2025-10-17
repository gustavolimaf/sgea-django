# Sistema de Gestão de Eventos Acadêmicos (SGEA)

## Documento de Requisitos e Casos de Uso

---

## 1. Introdução

### 1.1 Propósito

O Sistema de Gestão de Eventos Acadêmicos (SGEA) é uma plataforma web desenvolvida para facilitar o gerenciamento de eventos acadêmicos como seminários, palestras, minicursos e semanas acadêmicas.

### 1.2 Objetivos do Projeto

- Modelagem do sistema com requisitos funcionais e não funcionais
- Estruturação do projeto Django (apps, modelos, urls)
- Criação da lógica backend e modelos de banco de dados
- Prototipação de interface

### 1.3 Tecnologias

- **Framework:** Django (Python)
- **Banco de Dados:** SQLite
- **Frontend:** HTML5, CSS3
- **Geração de PDF:** ReportLab

---

## 2. Requisitos Funcionais

### RF01 - Cadastro de Usuários

**Descrição:** O sistema deve permitir que novos usuários se cadastrem na plataforma.

**Dados Necessários:**

- Nome completo (obrigatório)
- Telefone (obrigatório)
- Instituição de ensino (obrigatório para alunos e professores)
- E-mail/Usuário (obrigatório, único)
- Senha (obrigatório, mínimo 8 caracteres)
- Perfil: Aluno, Professor ou Organizador (obrigatório)

**Regras de Negócio:**

- O e-mail deve ser único no sistema
- A senha deve ter no mínimo 8 caracteres
- Alunos e professores devem informar a instituição de ensino

---

### RF02 - Autenticação de Usuários

**Descrição:** O sistema deve permitir que usuários façam login e logout.

**Funcionalidades:**

- Login com e-mail e senha
- Logout da sessão
- Redirecionamento baseado no perfil do usuário

**Regras de Negócio:**

- Credenciais devem ser validadas antes do acesso
- Senhas armazenadas com hash seguro
- Diferentes perfis têm permissões específicas

---

### RF03 - Cadastro de Eventos

**Descrição:** Organizadores podem criar e gerenciar eventos acadêmicos.

**Dados Necessários:**

- Tipo de evento (Seminário, Palestra, Minicurso, Semana Acadêmica)
- Nome do evento (obrigatório)
- Descrição (obrigatório)
- Data inicial e final (obrigatório)
- Horário de início e término (obrigatório)
- Local (obrigatório)
- Quantidade máxima de participantes (obrigatório)
- Organizador responsável (automático)

**Regras de Negócio:**

- Apenas organizadores podem criar eventos
- A data final não pode ser anterior à data inicial
- O número de participantes deve ser maior que zero

---

### RF04 - Inscrição de Usuários em Eventos

**Descrição:** Alunos e professores podem se inscrever em eventos disponíveis.

**Funcionalidades:**

- Listagem de eventos disponíveis
- Visualização de detalhes do evento
- Inscrição em evento
- Cancelamento de inscrição
- Visualização de "Minhas Inscrições"

**Regras de Negócio:**

- Usuários só podem se inscrever em eventos futuros
- Não é permitida inscrição duplicada
- Inscrição só se houver vagas disponíveis
- Sistema registra data/hora da inscrição automaticamente

---

### RF05 - Emissão de Certificados

**Descrição:** Organizadores podem emitir certificados em PDF para participantes.

**Funcionalidades:**

- Visualização de lista de inscritos
- Emissão de certificado
- Download de certificado em PDF
- Visualização de "Meus Certificados"
- Validação de certificado por código único

**Dados do Certificado:**

- Nome do participante
- Nome do evento
- Tipo de evento e carga horária
- Data do evento
- Local do evento
- Data de emissão
- Código de validação (UUID)

**Regras de Negócio:**

- Apenas organizadores podem emitir certificados
- Certificados só para usuários inscritos
- Um certificado por evento por usuário

---

## 3. Requisitos Não Funcionais

### RNF01 - Usabilidade

- Interface intuitiva e responsiva
- Mensagens de feedback claras
- Navegação consistente

### RNF02 - Segurança

- Senhas armazenadas com hash seguro
- Proteção contra SQL Injection (ORM Django)
- Proteção CSRF em formulários
- Validação de dados no backend

### RNF03 - Manutenibilidade

- Código seguindo padrão PEP 8
- Arquitetura MVT do Django bem definida
- Documentação completa (README, casos de uso)
- Versionamento com Git

---

## 4. Casos de Uso

### UC01 - Cadastro de Novo Usuário

**Ator Principal:** Visitante  
**Objetivo:** Cadastrar novo usuário no sistema

**Fluxo Principal:**

1. Visitante acessa a página de cadastro
2. Sistema exibe formulário com campos: nome, telefone, instituição, e-mail, senha, perfil
3. Visitante preenche os campos e submete
4. Sistema valida os dados
5. Sistema cria hash da senha
6. Sistema salva usuário no banco de dados
7. Sistema redireciona para página de login

**Fluxos Alternativos:**

- **FA01:** E-mail já cadastrado → Sistema exibe erro e solicita outro e-mail
- **FA02:** Senha inválida → Sistema exibe requisitos de senha
- **FA03:** Campos obrigatórios vazios → Sistema destaca campos pendentes

**Pós-condições:** Novo usuário criado e pode fazer login

---

### UC02 - Autenticação de Usuário

**Ator Principal:** Usuário cadastrado  
**Objetivo:** Fazer login no sistema

**Fluxo Principal:**

1. Usuário acessa a página de login
2. Sistema exibe formulário com e-mail e senha
3. Usuário preenche credenciais e submete
4. Sistema valida as credenciais
5. Sistema cria sessão de usuário
6. Sistema redireciona para dashboard conforme perfil

**Fluxos Alternativos:**

- **FA01:** Credenciais inválidas → Sistema exibe erro
- **FA02:** Campos vazios → Sistema destaca campos pendentes

**Pós-condições:** Usuário autenticado com sessão ativa

---

### UC03 - Criação de Evento

**Ator Principal:** Organizador  
**Objetivo:** Criar novo evento acadêmico

**Pré-condições:** Usuário autenticado como Organizador

**Fluxo Principal:**

1. Organizador acessa "Criar Evento"
2. Sistema exibe formulário com: tipo, nome, descrição, datas, horários, local, vagas
3. Organizador preenche os campos e submete
4. Sistema valida os dados (datas, horários, vagas)
5. Sistema associa organizador ao evento
6. Sistema salva evento no banco de dados
7. Sistema redireciona para detalhes do evento

**Fluxos Alternativos:**

- **FA01:** Usuário não é organizador → Sistema nega acesso (erro 403)
- **FA02:** Data final anterior à inicial → Sistema exibe erro de validação
- **FA03:** Número de vagas inválido → Sistema exibe erro

**Pós-condições:** Evento criado e disponível para inscrições

---

### UC04 - Inscrição em Evento

**Ator Principal:** Aluno ou Professor  
**Objetivo:** Inscrever-se em evento disponível

**Pré-condições:** Usuário autenticado, evento disponível com vagas

**Fluxo Principal:**

1. Usuário acessa lista de eventos disponíveis
2. Sistema exibe eventos com informações e vagas disponíveis
3. Usuário seleciona evento e clica em "Inscrever-se"
4. Sistema valida disponibilidade (vagas, data, duplicidade)
5. Sistema registra inscrição com data/hora
6. Sistema decrementa vagas disponíveis
7. Sistema exibe confirmação

**Fluxos Alternativos:**

- **FA01:** Evento sem vagas → Sistema exibe "Evento lotado"
- **FA02:** Usuário já inscrito → Sistema exibe "Já inscrito"
- **FA03:** Evento já iniciado → Sistema não permite inscrição

**Pós-condições:** Inscrição registrada e vaga ocupada

---

### UC05 - Emissão de Certificado

**Ator Principal:** Organizador  
**Objetivo:** Emitir certificado para participante do evento

**Pré-condições:** Usuário organizador, evento finalizado, participante inscrito

**Fluxo Principal:**

1. Organizador acessa lista de inscritos do evento
2. Sistema exibe inscritos com opção de marcar presença
3. Organizador marca presença do participante
4. Organizador clica em "Emitir Certificado"
5. Sistema verifica permissões e presença
6. Sistema gera certificado em PDF com dados do evento e participante
7. Sistema salva registro no banco de dados com código único (UUID)
8. Sistema disponibiliza download do PDF
9. Sistema exibe confirmação

**Fluxos Alternativos:**

- **FA01:** Certificado já emitido → Sistema exibe mensagem e link para download
- **FA02:** Participante sem presença → Sistema não permite emissão
- **FA03:** Evento não finalizado → Botão desabilitado

**Pós-condições:** Certificado emitido e disponível para download

---

## 5. Diagrama de Casos de Uso

```
                    Sistema SGEA
          ┌──────────────────────────┐
          │                          │
Visitante │  [UC01: Cadastrar-se]   │
   ───────┼─>                        │
          │                          │
────────────────────────────────────────
          │                          │
 Usuário  │  [UC02: Fazer Login]    │
   ───────┼─>                        │
          │                          │
────────────────────────────────────────
          │                          │
  Aluno/  │  [Listar Eventos]       │
Professor │  [UC04: Inscrever-se]   │
   ───────┼─> [Ver Inscrições]      │
          │   [Baixar Certificado]  │
          │                          │
────────────────────────────────────────
          │                          │
Organiza- │  [UC03: Criar Evento]   │
   dor    │  [Ver Inscritos]        │
   ───────┼─> [UC05: Emitir Certif.]│
          │                          │
          └──────────────────────────┘
```

---

## 6. Regras de Negócio Principais

| ID   | Descrição                                       |
| ---- | ----------------------------------------------- |
| RN01 | E-mail de usuário deve ser único no sistema     |
| RN02 | A senha deve ter no mínimo 8 caracteres         |
| RN03 | Alunos e professores devem informar instituição |
| RN04 | Apenas organizadores podem criar eventos        |
| RN05 | Data final não pode ser anterior à data inicial |
| RN06 | Inscrições só em eventos futuros com vagas      |
| RN07 | Não é permitida inscrição duplicada             |
| RN08 | Apenas organizadores podem emitir certificados  |
| RN09 | Certificados só para usuários inscritos         |
| RN10 | Um certificado por evento por usuário           |

---

**Documento gerado para o Sistema de Gestão de Eventos Acadêmicos (SGEA)**  
**Projeto Acadêmico - Disciplina de Desenvolvimento Web**  
**Data:** 16/10/2025
