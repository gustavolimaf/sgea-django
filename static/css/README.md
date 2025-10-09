# Arquivos CSS do SGEA

Esta pasta contém todos os arquivos CSS do Sistema de Gestão de Eventos Acadêmicos (SGEA), organizados de forma modular para facilitar a manutenção.

## Estrutura dos Arquivos

### `base.css`

**Propósito:** Estilos globais e componentes reutilizáveis

**Conteúdo:**

- Reset CSS e variáveis CSS customizadas (`:root`)
- Navbar e navegação
- Botões (primary, secondary, success, danger, outline)
- Container e layout
- Mensagens e alertas
- Footer
- Formulários (form-group, form-control, errorlist)
- Cards
- Grid system (grid-2, grid-3)
- Badges
- Utility classes (text-center, mt-_, mb-_)
- Media queries para responsividade

**Usado em:** Todos os templates (carregado no `base.html`)

---

### `home.css`

**Propósito:** Estilos específicos da página inicial

**Conteúdo:**

- Hero section com gradiente
- Stats section (estatísticas com cards)
- Event cards (cartões de eventos)
- Event vagas (barra de progresso)
- Features section
- CTA section (call-to-action)

**Usado em:** `home.html`

**Classe principal:** `.hero`

---

### `dashboard.css`

**Propósito:** Estilos para dashboards de usuários e organizadores

**Conteúdo:**

- Dashboard header e títulos
- Dashboard stats (estatísticas do usuário)
- Quick actions (ações rápidas)
- Event list (lista de eventos do dashboard)
- Empty state (estado vazio)

**Usado em:**

- `dashboard_usuario.html`
- `dashboard_organizador.html`

**Classes principais:** `.dashboard-stat-card`, `.quick-actions`

---

### `evento-inscritos.css`

**Propósito:** Estilos para página de gerenciamento de inscritos

**Conteúdo:**

- Evento info header (cabeçalho com informações do evento)
- Stats grid (grid de estatísticas)
- Inscritos table (tabela de participantes)
- Search box (caixa de busca)
- Action buttons (botões de ação)
- Certificate badges (badges de certificados)

**Usado em:** `evento_inscritos.html`

**Classes principais:** `.inscritos-table`, `.search-input`, `.certificado-badge`

---

### `certificado.css`

**Propósito:** Estilos para geração de certificados PDF

**Conteúdo:**

- Configuração de página A4 landscape (`@page`)
- Container do certificado com gradiente
- Header, body e footer do certificado
- Assinaturas
- Código de verificação
- Ornamentos decorativos
- Media queries para impressão

**Usado em:** `certificado_pdf.html`

**Classes principais:** `.certificado-container`, `.certificado-body`

**Observações:**

- Otimizado para impressão
- Usa WeasyPrint para renderização PDF

---

## Como Usar

### 1. Carregar CSS no Template Base

```html
{% load static %} <link rel="stylesheet" href="{% static 'css/base.css' %}" />
```

### 2. Carregar CSS Específico em Outros Templates

```html
{% block extra_css %} {% load static %}
<link rel="stylesheet" href="{% static 'css/home.css' %}" />
{% endblock %}
```

### 3. Ordem de Carregamento

1. `base.css` (sempre primeiro, carregado no base.html)
2. CSS específico da página (no bloco `extra_css`)

---

## Variáveis CSS Disponíveis

Todas as variáveis estão definidas em `base.css`:

```css
:root {
  --primary-color: #2563eb; /* Azul principal */
  --primary-dark: #1e40af; /* Azul escuro */
  --secondary-color: #64748b; /* Cinza */
  --success-color: #10b981; /* Verde */
  --danger-color: #ef4444; /* Vermelho */
  --warning-color: #f59e0b; /* Amarelo */
  --info-color: #3b82f6; /* Azul info */
  --light-bg: #f8fafc; /* Fundo claro */
  --dark-text: #1e293b; /* Texto escuro */
  --border-color: #e2e8f0; /* Borda */
}
```

**Uso:**

```css
.meu-elemento {
  color: var(--primary-color);
  background-color: var(--light-bg);
}
```

---

## Convenções de Nomenclatura

### Classes de Componentes

- Use nomes descritivos: `.evento-card`, `.stat-number`
- Use hífen para separar palavras: `.quick-action-btn`

### Classes de Utilidade

- Prefixos padrão: `text-`, `mt-`, `mb-`
- Exemplo: `.text-center`, `.mt-4`, `.mb-2`

### Classes de Estado

- Sufixos: `-active`, `-disabled`, `-hover`
- Exemplo: `.btn-primary:hover`

---

## Responsividade

Breakpoints padrão definidos em `base.css`:

```css
/* Mobile: < 768px */
@media (max-width: 768px) {
  /* Ajustes para mobile */
}
```

---

## Manutenção

### Adicionar Novo Estilo

1. Determine se é global (→ `base.css`) ou específico (→ criar novo arquivo)
2. Use as variáveis CSS existentes quando possível
3. Siga as convenções de nomenclatura
4. Adicione comentários explicativos

### Modificar Estilo Existente

1. Identifique o arquivo correto usando este README
2. Localize a classe ou seletor
3. Faça a alteração mantendo consistência
4. Teste em diferentes dispositivos

---

## Comandos Úteis

### Coletar Arquivos Estáticos para Produção

```bash
python manage.py collectstatic
```

### Verificar Arquivos Estáticos Carregados

Abra o DevTools do navegador e veja a aba "Network" → "CSS"

---

## Arquivos de Template Correspondentes

| Arquivo CSS            | Templates                                              |
| ---------------------- | ------------------------------------------------------ |
| `base.css`             | Todos (via `base.html`)                                |
| `home.css`             | `home.html`                                            |
| `dashboard.css`        | `dashboard_usuario.html`, `dashboard_organizador.html` |
| `evento-inscritos.css` | `evento_inscritos.html`                                |
| `certificado.css`      | `certificado_pdf.html`                                 |

---

## Estrutura de Diretórios

```
sgea-django/
├── static/
│   └── css/
│       ├── base.css              (Estilos globais)
│       ├── home.css              (Página inicial)
│       ├── dashboard.css         (Dashboards)
│       ├── evento-inscritos.css  (Gerenciamento)
│       ├── certificado.css       (Certificados PDF)
│       └── README.md             (Este arquivo)
├── eventos/
│   └── templates/
│       └── eventos/
│           ├── base.html         (Template base)
│           ├── home.html
│           ├── dashboard_*.html
│           └── ...
└── manage.py
```

---

**Última atualização:** Outubro 2025  
**Versão:** 1.0.0
