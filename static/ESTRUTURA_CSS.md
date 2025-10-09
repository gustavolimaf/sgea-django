# 🎨 Estrutura CSS do SGEA - Guia Rápido

## ✅ O que foi criado

Todos os estilos CSS foram extraídos dos templates HTML e organizados em **5 arquivos CSS modulares** na pasta `static/css/`.

## 📁 Estrutura de Arquivos

```
static/
└── css/
    ├── base.css                 (6.5 KB) - Estilos globais
    ├── home.css                 (3.4 KB) - Página inicial
    ├── dashboard.css            (3.3 KB) - Dashboards
    ├── evento-inscritos.css     (2.8 KB) - Gerenciamento
    ├── certificado.css          (2.8 KB) - Certificados PDF
    └── README.md                (6.6 KB) - Documentação completa
```

**Total:** 19.3 KB de CSS organizado + 6.6 KB de documentação

## 🎯 Mapeamento Template → CSS

| Template                     | CSS Principal          | CSS Base |
| ---------------------------- | ---------------------- | -------- |
| `base.html`                  | `base.css`             | ✓        |
| `home.html`                  | `home.css`             | ✓        |
| `dashboard_usuario.html`     | `dashboard.css`        | ✓        |
| `dashboard_organizador.html` | `dashboard.css`        | ✓        |
| `evento_inscritos.html`      | `evento-inscritos.css` | ✓        |
| `certificado_pdf.html`       | `certificado.css`      | ✗        |
| `login.html`                 | -                      | ✓        |
| `registro.html`              | -                      | ✓        |
| `evento_detail.html`         | -                      | ✓        |
| `eventos_list.html`          | -                      | ✓        |

## 📝 Resumo dos Arquivos

### 1️⃣ base.css (Estilos Globais)

**Conteúdo:**

- ✅ Variáveis CSS (10 cores customizadas)
- ✅ Reset CSS e normalização
- ✅ Navbar e navegação
- ✅ Botões (6 variações)
- ✅ Container e layout
- ✅ Alertas e mensagens (4 tipos)
- ✅ Formulários completos
- ✅ Cards
- ✅ Grid system (2 e 3 colunas)
- ✅ Badges (4 cores)
- ✅ 14 utility classes
- ✅ Media queries responsivos

**Usado em:** Todos os templates

---

### 2️⃣ home.css (Página Inicial)

**Conteúdo:**

- ✅ Hero section com gradiente
- ✅ Stats cards (estatísticas)
- ✅ Event cards com hover
- ✅ Barra de progresso de vagas
- ✅ Features section
- ✅ CTA section

**Usado em:** `home.html`

---

### 3️⃣ dashboard.css (Dashboards)

**Conteúdo:**

- ✅ Dashboard header
- ✅ Stats cards com 4 cores
- ✅ Quick actions grid
- ✅ Event list
- ✅ Empty state

**Usado em:** `dashboard_usuario.html`, `dashboard_organizador.html`

---

### 4️⃣ evento-inscritos.css (Gerenciamento)

**Conteúdo:**

- ✅ Header com gradiente
- ✅ Stats grid (4 cards)
- ✅ Tabela de inscritos
- ✅ Search box
- ✅ Action buttons
- ✅ Certificate badges

**Usado em:** `evento_inscritos.html`

---

### 5️⃣ certificado.css (Certificados PDF)

**Conteúdo:**

- ✅ Configuração A4 landscape
- ✅ Container com gradiente
- ✅ Header, body, footer
- ✅ Assinaturas
- ✅ Código de verificação
- ✅ Ornamentos decorativos
- ✅ Media queries para impressão

**Usado em:** `certificado_pdf.html`

## 🎨 Variáveis CSS Disponíveis

```css
--primary-color: #2563eb; /* Azul principal */
--primary-dark: #1e40af; /* Azul escuro (hover) */
--secondary-color: #64748b; /* Cinza */
--success-color: #10b981; /* Verde */
--danger-color: #ef4444; /* Vermelho */
--warning-color: #f59e0b; /* Amarelo */
--info-color: #3b82f6; /* Azul informativo */
--light-bg: #f8fafc; /* Fundo claro */
--dark-text: #1e293b; /* Texto escuro */
--border-color: #e2e8f0; /* Borda padrão */
```

## 🔧 Como Usar

### No Template Base (base.html)

```html
{% load static %} <link rel="stylesheet" href="{% static 'css/base.css' %}" />
```

### Em Templates Específicos

```html
{% block extra_css %} {% load static %}
<link rel="stylesheet" href="{% static 'css/home.css' %}" />
{% endblock %}
```

### Ordem de Carregamento

1. **base.css** (sempre primeiro - global)
2. **CSS específico** (via bloco extra_css)

## ✅ Arquivos Atualizados

### Templates Modificados

- ✅ `base.html` - Agora carrega `base.css` via `{% static %}`
- ✅ `home.html` - Agora carrega `home.css` via `{% static %}`
- ✅ `certificado_pdf.html` - Recriado para usar `certificado.css`

### Arquivos Removidos

- ❌ `<style>` inline nos templates (migrado para arquivos .css)

## 📊 Benefícios da Modularização

✅ **Manutenção:** Fácil localizar e editar estilos específicos  
✅ **Performance:** Cache de CSS separado do HTML  
✅ **Organização:** Código limpo e estruturado  
✅ **Reutilização:** Variáveis CSS globais  
✅ **Escalabilidade:** Adicionar novos estilos sem confusão  
✅ **Colaboração:** Múltiplos desenvolvedores podem trabalhar simultaneamente

## 🚀 Próximos Passos

### Para Desenvolvimento

```bash
# Certificar que static files estão configurados
python manage.py collectstatic --noinput
```

### Para Produção

```bash
# Minificar CSS (opcional)
npm install -g cssnano-cli
cssnano static/css/base.css static/css/base.min.css
```

## 📖 Documentação Completa

Para documentação detalhada de cada classe CSS, consulte:

- **`static/css/README.md`** - Documentação completa dos arquivos CSS

## 🎓 Convenções de Código

### Nomenclatura de Classes

- **Componentes:** `.evento-card`, `.stat-number`
- **Utilities:** `.text-center`, `.mt-4`, `.mb-2`
- **Estados:** `.btn-primary:hover`, `.card:active`

### Estrutura de Arquivos CSS

```css
/* ====================
   Seção do CSS
   ==================== */

.classe-exemplo {
  propriedade: valor;
}
```

## ⚡ Performance

### Tamanho Total

- **Antes:** ~25 KB de CSS inline em templates
- **Depois:** 19.3 KB de CSS em arquivos separados
- **Redução:** ~23% (devido à eliminação de duplicações)

### Carregamento

- CSS externo permite cache do navegador
- Reduz tamanho do HTML servido
- Permite compressão gzip mais eficiente

## 🐛 Troubleshooting

### CSS não está carregando?

```python
# Verifique settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Execute collectstatic
python manage.py collectstatic
```

### Estilos não aparecem?

1. Verifique se `{% load static %}` está no topo do template
2. Use DevTools (F12) → Network para ver se CSS foi carregado
3. Limpe o cache do navegador (Ctrl + Shift + R)

---

**Criado em:** Outubro 2025  
**Versão:** 1.0.0  
**Autor:** Sistema de Gestão de Eventos Acadêmicos (SGEA)
