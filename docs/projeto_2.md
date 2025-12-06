# **Fase 2 do Projeto: Sistema de Gestão de Eventos Acadêmicos (SGEA)**

Esta fase concentra-se em aprimorar a interação do usuário, robustecer as regras de negócio, introduzir a automação de processos e expandir a arquitetura do sistema com uma API REST.

## **1\. Validação Avançada de Formulários**

A validação será aprimorada para garantir a integridade dos dados.

* **Telefone:** Implementar máscara de entrada no formato (XX) XXXXX-XXXX.  
* **Data e Horário:** Utilizar seletor (*datepicker/timepicker*), como os da biblioteca JQuery.  
* **Integridade:** Identificar valores inválidos em campos como e-mail e número de participantes.  
* **Imagens:** Validar arquivos de banners (verificar se é imagem) antes da conclusão do cadastro.

## **2\. Carga Inicial de Dados (Seeding)**

Dados iniciais para testes e demonstração.

| Tipo de Usuário | Login | Senha |
| :---- | :---- | :---- |
| **Organizador** | organizador@sgea.com | Admin@123 |
| **Aluno** | aluno@sgea.com | Aluno@123 |
| **Professor** | professor@sgea.com | Professor@123 |

## **3\. API REST (Consulta e Inscrição)**

Desenvolvida com **djangorestframework**. Exige autenticação (Login/Senha \-\> Token).

### **Funcionalidades**

1. **Consulta de Eventos:** Listar nome, data, local e organizador responsável.  
2. **Inscrição de Participantes:** Permitir inscrição de usuários já cadastrados.

### **Limitação de Requisições (Throttling)**

* **Consulta de Eventos:** 20 requisições por dia.  
* **Inscrições de Participantes:** 50 requisições por dia.

## **4\. Banner do Evento**

* Inclusão de campo para upload de imagem (banner) no cadastro de eventos.  
* Exibição na página de detalhes.  
* Validação obrigatória do tipo de arquivo.

## **5\. Documentação do Projeto (GitHub)**

Deve ser expandida para incluir:

* **Guia de Instalação:** Configuração de ambiente, dependências e execução.  
* **Guia de Testes:** Roteiro de testes e orientações para popular o banco de dados.

## **6\. Regras de Negócio**

1. **Datas:** Proibido cadastrar eventos com data de início anterior à atual.  
2. **Responsável:** Todo evento deve ter um professor responsável vinculado.  
3. **Vagas:** Bloquear inscrições quando o limite de vagas for atingido.  
4. **Duplicidade:** Usuário não pode se inscrever mais de uma vez no mesmo evento.  
5. **Segurança de Senha:**  
   * Mínimo 8 caracteres.  
   * Deve conter letras, números e caracteres especiais.  
   * Obrigatório campo de confirmação de senha.

## **7\. Notificação por E-mail**

Envio automático após cadastro contendo:

* Saudação de boas-vindas.  
* Logo do SGEA.  
* Nome do usuário.  
* **Link ou código de acesso.**

**Nota:** Novos usuários só acessam o sistema após a confirmação da inscrição via link/código.

## **8\. Emissão Automática de Certificados**

Gerados automaticamente após o término do evento para usuários com presença confirmada.

## **9\. Perfis de Usuário e Permissões**

### **Aluno e Professor**

* Podem se inscrever e cancelar inscrições.  
* Podem consultar certificados próprios.  
* *Professor:* Pode ser vinculado como responsável por evento.

### **Organizador**

* Cadastrar, alterar e excluir eventos.  
* Cadastrar novos participantes.  
* Consultar registros de auditoria.  
* **Restrição:** Não deve realizar inscrições para eventos.

## **10\. Registros de Auditoria (Logs)**

O sistema deve registrar ações críticas para rastreabilidade:

* Criação de novos usuários.  
* Cadastro, alteração e exclusão de eventos.  
* Consultas via API.  
* Geração e consulta de certificados.  
* Inscrição em eventos.

**Visualização:** O Organizador deve ter uma tela para consultar ações por dia ou por usuário específico.

## **11\. Identificação Visual**

* Folhas de estilo (CSS) com identidade visual definida (cores e ícones padronizados).  
* Nome próprio e logotipo do sistema.  
* Conformidade com padrões internacionais de **Usabilidade** e **Acessibilidade**.

## **Tabela de Avaliação \- Fase 2**

| Critério | Peso |
| :---- | :---- |
| Implementação da API REST (Consulta e Inscrição) | 2.0 |
| Validações e Regras de Negócio | 1.5 |
| Aplicação de Identidade Visual | 1.5 |
| Automação (Envio de E-mail e Emissão de Certificados) | 1.0 |
| Documentação Técnica (Instalação e Testes) | 1.0 |
| Implementação dos Perfis de Usuário, com controle de acesso | 1.5 |
| Auditoria das funções | 1.5 |
| **Total** | **10.0** |

