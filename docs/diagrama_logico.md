# Diagrama Lógico do Banco de Dados - SGEA

## Descrição Geral

O banco de dados do Sistema de Gestão de Eventos Acadêmicos (SGEA) é composto por 4 tabelas principais que implementam toda a lógica de negócio do sistema.

---

## Estrutura das Tabelas

### 1. eventos_usuario

Tabela que armazena os usuários do sistema com autenticação Django.

**Campos:**

| Campo         | Tipo         | Restrições          | Descrição                     |
| ------------- | ------------ | ------------------- | ----------------------------- |
| id            | INTEGER      | PK, AUTO_INCREMENT  | Identificador único           |
| username      | VARCHAR(150) | NOT NULL, UNIQUE    | Nome de usuário para login    |
| password      | VARCHAR(128) | NOT NULL            | Senha hasheada                |
| email         | VARCHAR(254) | NOT NULL, UNIQUE    | Email do usuário              |
| first_name    | VARCHAR(30)  | NOT NULL            | Primeiro nome                 |
| last_name     | VARCHAR(150) | NOT NULL            | Sobrenome                     |
| telefone      | VARCHAR(15)  | NOT NULL            | Telefone de contato           |
| instituicao   | VARCHAR(200) | NULL                | Instituição de ensino         |
| perfil        | VARCHAR(12)  | NOT NULL            | ALUNO, PROFESSOR, ORGANIZADOR |
| is_active     | BOOLEAN      | NOT NULL, DEFAULT 1 | Indica se está ativo          |
| is_staff      | BOOLEAN      | NOT NULL, DEFAULT 0 | Acesso ao admin               |
| is_superuser  | BOOLEAN      | NOT NULL, DEFAULT 0 | Superusuário                  |
| date_joined   | DATETIME     | NOT NULL            | Data de cadastro              |
| last_login    | DATETIME     | NULL                | Último login                  |
| data_cadastro | DATETIME     | NOT NULL            | Data do cadastro no SGEA      |

**Índices:**

- `idx_usuario_perfil` em (perfil)
- `idx_usuario_email` em (email)

**Restrições:**

- CHECK: perfil IN ('ALUNO', 'PROFESSOR', 'ORGANIZADOR')
- Validação: instituição obrigatória para ALUNO e PROFESSOR

---

### 2. eventos_evento

Tabela que armazena os eventos acadêmicos.

**Campos:**

| Campo            | Tipo         | Restrições          | Descrição                 | On Delete |
| ---------------- | ------------ | ------------------- | ------------------------- | --------- |
| id               | INTEGER      | PK, AUTO_INCREMENT  | Identificador único       | -         |
| tipo             | VARCHAR(20)  | NOT NULL            | Tipo do evento            | -         |
| nome             | VARCHAR(200) | NOT NULL            | Nome do evento            | -         |
| descricao        | TEXT         | NOT NULL            | Descrição detalhada       | -         |
| data_inicial     | DATE         | NOT NULL            | Data de início            | -         |
| data_final       | DATE         | NOT NULL            | Data de término           | -         |
| horario_inicio   | TIME         | NOT NULL            | Horário de início         | -         |
| horario_fim      | TIME         | NOT NULL            | Horário de término        | -         |
| local            | VARCHAR(300) | NOT NULL            | Local do evento           | -         |
| vagas_totais     | INTEGER      | NOT NULL            | Total de vagas            | -         |
| organizador_id   | INTEGER      | FK, NOT NULL        | Referência ao organizador | PROTECT   |
| ativo            | BOOLEAN      | NOT NULL, DEFAULT 1 | Status do evento          | -         |
| data_criacao     | DATETIME     | NOT NULL            | Data de criação           | -         |
| data_atualizacao | DATETIME     | NOT NULL            | Última atualização        | -         |

**Índices:**

- `idx_evento_data_inicial` em (data_inicial)
- `idx_evento_tipo` em (tipo)
- `idx_evento_organizador` em (organizador_id)
- `idx_evento_ativo` em (ativo)

**Restrições:**

- CHECK: tipo IN ('SEMINARIO', 'PALESTRA', 'MINICURSO', 'SEMANA_ACADEMICA')
- CHECK: vagas_totais > 0
- CHECK: data_final >= data_inicial
- FK: organizador_id REFERENCES eventos_usuario(id)

---

### 3. eventos_inscricao

Tabela que registra as inscrições de usuários em eventos.

**Campos:**

| Campo             | Tipo     | Restrições          | Descrição              | On Delete |
| ----------------- | -------- | ------------------- | ---------------------- | --------- |
| id                | INTEGER  | PK, AUTO_INCREMENT  | Identificador único    | -         |
| usuario_id        | INTEGER  | FK, NOT NULL        | Referência ao usuário  | CASCADE   |
| evento_id         | INTEGER  | FK, NOT NULL        | Referência ao evento   | CASCADE   |
| data_inscricao    | DATETIME | NOT NULL            | Data/hora da inscrição | -         |
| ativa             | BOOLEAN  | NOT NULL, DEFAULT 1 | Status da inscrição    | -         |
| data_cancelamento | DATETIME | NULL                | Data do cancelamento   | -         |

**Índices:**

- `idx_inscricao_usuario_ativa` em (usuario_id, ativa)
- `idx_inscricao_evento_ativa` em (evento_id, ativa)

**Restrições:**

- UNIQUE: (usuario_id, evento_id) - Evita inscrição duplicada
- FK: usuario_id REFERENCES eventos_usuario(id) ON DELETE CASCADE
- FK: evento_id REFERENCES eventos_evento(id) ON DELETE CASCADE

---

### 4. eventos_certificado

Tabela que armazena os certificados emitidos.

**Campos:**

| Campo              | Tipo         | Restrições           | Descrição                        | On Delete |
| ------------------ | ------------ | -------------------- | -------------------------------- | --------- |
| id                 | INTEGER      | PK, AUTO_INCREMENT   | Identificador único              | -         |
| inscricao_id       | INTEGER      | FK, NOT NULL, UNIQUE | Referência à inscrição           | CASCADE   |
| codigo_verificacao | VARCHAR(50)  | NOT NULL, UNIQUE     | Código único de verificação      | -         |
| data_emissao       | DATETIME     | NOT NULL             | Data de emissão                  | -         |
| emitido_por_id     | INTEGER      | FK, NOT NULL         | Organizador que emitiu           | PROTECT   |
| arquivo_pdf        | VARCHAR(100) | NULL                 | Caminho do PDF (FileField/media) | -         |

**Índices:**

- `idx_certificado_codigo` em (codigo_verificacao)

**Restrições:**

- FK: inscricao_id REFERENCES eventos_inscricao(id) ON DELETE CASCADE
- FK: emitido_por_id REFERENCES eventos_usuario(id)
- UNIQUE: inscricao_id - Um certificado por inscrição

---

## Diagrama de Relacionamentos

```
┌─────────────────────────┐
│   eventos_usuario       │
│─────────────────────────│
│ PK id                   │
│    username             │
│    email                │
│    first_name           │
│    last_name            │
│    telefone             │
│    instituicao          │
│    perfil               │
│    ...                  │
└─────────────────────────┘
       │ 1                │ 1
       │                  │
       │ organizador      │ emitido_por
       │                  │
       ▼ N                ▼ N
┌─────────────────────────┐    ┌─────────────────────────┐
│   eventos_evento        │    │  eventos_certificado    │
│─────────────────────────│    │─────────────────────────│
│ PK id                   │    │ PK id                   │
│    tipo                 │    │ FK inscricao_id (UNIQUE)│
│    nome                 │    │    codigo_verificacao   │
│    descricao            │    │    data_emissao         │
│    data_inicial         │    │ FK emitido_por_id       │
│    data_final           │    │    arquivo_pdf          │
│    horario_inicio       │    └─────────────────────────┘
│    horario_fim          │              ▲ 1
│    local                │              │
│    vagas_totais         │              │
│ FK organizador_id       │              │
│    ativo                │              │
│    ...                  │              │
└─────────────────────────┘              │
       │ 1                               │
       │                                 │
       │                                 │
       ▼ N                               │
┌─────────────────────────┐              │
│  eventos_inscricao      │              │
│─────────────────────────│              │
│ PK id                   │──────────────┘ 1
│ FK usuario_id           │
│ FK evento_id            │
│    data_inscricao       │
│    ativa                │
│    data_cancelamento    │
└─────────────────────────┘
       ▲ N
       │
       │
       │ 1
┌─────────────────────────┐
│   eventos_usuario       │
│      (participante)     │
└─────────────────────────┘
```

---

## Relacionamentos Detalhados

### 1. Usuario → Evento (1:N)

- **Tipo**: Um para Muitos
- **Chave Estrangeira**: eventos_evento.organizador_id
- **Descrição**: Um usuário organizador pode criar vários eventos

### 2. Usuario → Inscricao (1:N)

- **Tipo**: Um para Muitos
- **Chave Estrangeira**: eventos_inscricao.usuario_id
- **Descrição**: Um usuário pode ter várias inscrições
- **Regra**: ON DELETE CASCADE

### 3. Evento → Inscricao (1:N)

- **Tipo**: Um para Muitos
- **Chave Estrangeira**: eventos_inscricao.evento_id
- **Descrição**: Um evento pode ter várias inscrições
- **Regra**: ON DELETE CASCADE

### 4. Inscricao → Certificado (1:1)

- **Tipo**: Um para Um
- **Chave Estrangeira**: eventos_certificado.inscricao_id (UNIQUE)
- **Descrição**: Cada inscrição pode ter apenas um certificado

### 5. Usuario → Certificado (1:N)

- **Tipo**: Um para Muitos
- **Chave Estrangeira**: eventos_certificado.emitido_por_id
- **Descrição**: Um organizador pode emitir vários certificados

---

## Regras de Integridade

### Constraints de Banco de Dados

1. **Perfil válido**: perfil deve ser 'ALUNO', 'PROFESSOR' ou 'ORGANIZADOR'
2. **Tipo de evento válido**: tipo deve ser 'SEMINARIO', 'PALESTRA', 'MINICURSO' ou 'SEMANA_ACADEMICA'
3. **Vagas positivas**: vagas_totais > 0
4. **Datas válidas**: data_final >= data_inicial
5. **Inscrição única**: Um usuário não pode se inscrever duas vezes no mesmo evento (UNIQUE constraint)
6. **Certificado único**: Uma inscrição só pode ter um certificado (OneToOne relationship)

### Validações de Negócio (Implementadas no Código)

1. **Instituição obrigatória**: Campo `instituicao` é obrigatório para usuários com perfil ALUNO ou PROFESSOR (exceto superusuários e staff)

2. **Horário válido**: Em eventos de um único dia (data_inicial = data_final), o horário de término deve ser posterior ao horário de início

3. **Evento já ocorrido**: Não é permitido se inscrever em eventos cuja data final já passou

4. **Vagas disponíveis**: Não é permitido se inscrever em eventos lotados (vagas_disponiveis <= 0)

5. **Inscrição ativa**: Certificados só podem ser emitidos para inscrições com status `ativa=True`

6. **Autorização para emitir**: Apenas o organizador do evento pode emitir certificados para aquele evento

7. **Código único**: Certificados recebem automaticamente um código de verificação único (UUID) se não fornecido

---

## Properties e Métodos Calculados

### Modelo Evento

| Property/Método   | Tipo | Descrição                                                               |
| ----------------- | ---- | ----------------------------------------------------------------------- |
| vagas_disponiveis | int  | Retorna o número de vagas disponíveis (vagas_totais - inscritos ativos) |
| esta_lotado       | bool | Retorna True se não há mais vagas disponíveis                           |
| ja_ocorreu        | bool | Retorna True se a data_final já passou                                  |
| duracao_horas     | int  | Calcula a duração total do evento em horas                              |

### Modelo Inscricao

| Método   | Retorno | Descrição                                                   |
| -------- | ------- | ----------------------------------------------------------- |
| cancelar | None    | Marca a inscrição como inativa e registra data_cancelamento |

### Modelo Certificado

| Método | Retorno | Descrição                                                     |
| ------ | ------- | ------------------------------------------------------------- |
| save   | None    | Gera automaticamente código_verificacao (UUID) se não existir |

---

## Observações Técnicas

1. **SQLite** foi escolhido para facilitar desenvolvimento e testes
2. Todos os campos de data/hora usam timezone-aware do Django
3. Senhas são armazenadas com PBKDF2 SHA256 (padrão Django)
4. Índices foram criados em campos frequentemente consultados para otimizar queries
5. Foreign Keys com CASCADE e PROTECT foram estrategicamente definidas:
   - **CASCADE**: Quando o registro pai é deletado, os filhos também são (inscrições e certificados)
   - **PROTECT**: Impede a deleção se houver registros relacionados (organizador de evento, emissor de certificado)
6. O campo `arquivo_pdf` usa FileField do Django, armazenado em `media/certificados/YYYY/MM/`

### Pendências de Migration

⚠️ **Importante**: Após atualizar o código, execute:

```bash
python manage.py makemigrations eventos --name add_ativo_index
python manage.py migrate
```

Isso criará o índice no campo `ativo` da tabela `eventos_evento`.

---

**Última atualização**: 16 de Outubro de 2025
