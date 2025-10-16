"""
Configuração do Django Admin para o SGEA
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Usuario, Evento, Inscricao, Certificado


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Admin para o modelo Usuario"""
    list_display = [
        "username", "email", "first_name", "last_name", 
        "perfil", "instituicao", "is_active", "data_cadastro"
    ]
    list_filter = ["perfil", "is_active", "is_staff", "data_cadastro"]
    search_fields = ["username", "email", "first_name", "last_name", "instituicao"]
    ordering = ["-data_cadastro"]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Informações Adicionais", {
            "fields": ("telefone", "instituicao", "perfil", "data_cadastro")
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Informações Adicionais", {
            "fields": ("telefone", "instituicao", "perfil")
        }),
    )
    
    readonly_fields = ["data_cadastro"]


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Admin para o modelo Evento"""
    list_display = [
        "nome", "tipo", "data_inicial", "data_final",
        "vagas_display", "organizador", "ativo_badge"
    ]
    list_filter = ["tipo", "ativo", "data_inicial", "data_criacao"]
    search_fields = ["nome", "descricao", "local"]
    date_hierarchy = "data_inicial"
    ordering = ["-data_inicial"]
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("tipo", "nome", "descricao", "ativo")
        }),
        ("Data e Horário", {
            "fields": (
                ("data_inicial", "data_final"),
                ("horario_inicio", "horario_fim")
            )
        }),
        ("Local e Capacidade", {
            "fields": ("local", "vagas_totais")
        }),
        ("Organização", {
            "fields": ("organizador",)
        }),
        ("Metadados", {
            "fields": ("data_criacao", "data_atualizacao"),
            "classes": ("collapse",)
        }),
    )
    
    readonly_fields = ["data_criacao", "data_atualizacao"]
    
    def vagas_display(self, obj):
        inscritos = obj.inscricoes.filter(ativa=True).count()
        percentual = (inscritos / obj.vagas_totais) * 100 if obj.vagas_totais > 0 else 0
        
        if percentual >= 90:
            color = "red"
        elif percentual >= 70:
            color = "orange"
        else:
            color = "green"
        
        return format_html(
            '<span style="color: {};">{}/{} ({:.0f}%)</span>',
            color, inscritos, obj.vagas_totais, percentual
        )
    vagas_display.short_description = "Vagas"
    
    def ativo_badge(self, obj):
        if obj.ativo:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 3px 10px; border-radius: 3px;">Ativo</span>'
            )
        return format_html(
            '<span style="background-color: #ef4444; color: white; padding: 3px 10px; border-radius: 3px;">Inativo</span>'
        )
    ativo_badge.short_description = "Status"


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    """Admin para o modelo Inscricao"""
    list_display = [
        "usuario_nome", "evento_nome", "data_inscricao",
        "ativa_badge", "tem_certificado"
    ]
    list_filter = ["ativa", "data_inscricao", "evento__tipo"]
    search_fields = [
        "usuario__first_name", "usuario__last_name",
        "usuario__email", "evento__nome"
    ]
    date_hierarchy = "data_inscricao"
    ordering = ["-data_inscricao"]
    
    fieldsets = (
        ("Inscrição", {
            "fields": ("usuario", "evento", "ativa")
        }),
        ("Datas", {
            "fields": ("data_inscricao", "data_cancelamento")
        }),
    )
    
    readonly_fields = ["data_inscricao"]
    
    def usuario_nome(self, obj):
        return obj.usuario.get_full_name()
    usuario_nome.short_description = "Usuário"
    usuario_nome.admin_order_field = "usuario__first_name"
    
    def evento_nome(self, obj):
        return obj.evento.nome
    evento_nome.short_description = "Evento"
    evento_nome.admin_order_field = "evento__nome"
    
    def ativa_badge(self, obj):
        if obj.ativa:
            return format_html(
                '<span style="background-color: #10b981; color: white; padding: 3px 10px; border-radius: 3px;">Ativa</span>'
            )
        return format_html(
            '<span style="background-color: #6b7280; color: white; padding: 3px 10px; border-radius: 3px;">Cancelada</span>'
        )
    ativa_badge.short_description = "Status"
    
    def tem_certificado(self, obj):
        if hasattr(obj, "certificado"):
            return format_html("Sim")
        return format_html("Não")
    tem_certificado.short_description = "Certificado"


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    """Admin para o modelo Certificado"""
    list_display = [
        "codigo_verificacao", "participante_nome",
        "evento_nome", "data_emissao", "emitido_por_nome"
    ]
    list_filter = ["data_emissao", "inscricao__evento__tipo"]
    search_fields = [
        "codigo_verificacao",
        "inscricao__usuario__first_name",
        "inscricao__usuario__last_name",
        "inscricao__evento__nome"
    ]
    date_hierarchy = "data_emissao"
    ordering = ["-data_emissao"]
    
    fieldsets = (
        ("Certificado", {
            "fields": ("inscricao", "codigo_verificacao", "emitido_por")
        }),
        ("Arquivo", {
            "fields": ("arquivo_pdf",)
        }),
        ("Metadados", {
            "fields": ("data_emissao",),
            "classes": ("collapse",)
        }),
    )
    
    readonly_fields = ["codigo_verificacao", "data_emissao"]
    
    def participante_nome(self, obj):
        return obj.inscricao.usuario.get_full_name()
    participante_nome.short_description = "Participante"
    
    def evento_nome(self, obj):
        return obj.inscricao.evento.nome
    evento_nome.short_description = "Evento"
    
    def emitido_por_nome(self, obj):
        return obj.emitido_por.get_full_name()
    emitido_por_nome.short_description = "Emitido Por"


# Personalização do Admin Site
admin.site.site_header = "SGEA - Administração"
admin.site.site_title = "SGEA Admin"
admin.site.index_title = "Gestão de Eventos Acadêmicos"
