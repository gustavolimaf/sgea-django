from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento, Inscricao, Certificado


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuração do admin para o modelo Usuario
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'perfil', 'instituicao', 'is_staff')
    list_filter = ('perfil', 'is_staff', 'is_active', 'data_cadastro')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'instituicao')
    ordering = ('-data_cadastro',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('telefone', 'instituicao', 'perfil', 'data_cadastro')
        }),
    )
    
    readonly_fields = ('data_cadastro',)
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('telefone', 'instituicao', 'perfil')
        }),
    )


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Evento
    """
    list_display = ('nome', 'tipo', 'data_inicial', 'data_final', 'local', 'vagas_totais', 'get_vagas_disponiveis', 'organizador', 'ativo')
    list_filter = ('tipo', 'ativo', 'data_inicial', 'organizador')
    search_fields = ('nome', 'descricao', 'local', 'organizador__username')
    date_hierarchy = 'data_inicial'
    ordering = ('-data_inicial',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('tipo', 'nome', 'descricao')
        }),
        ('Data e Horário', {
            'fields': ('data_inicial', 'data_final', 'horario_inicio', 'horario_fim')
        }),
        ('Local e Vagas', {
            'fields': ('local', 'vagas_totais')
        }),
        ('Organização', {
            'fields': ('organizador', 'ativo')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_criacao', 'data_atualizacao')
    
    def get_vagas_disponiveis(self, obj):
        """Retorna o número de vagas disponíveis"""
        return obj.vagas_disponiveis
    get_vagas_disponiveis.short_description = 'Vagas Disponíveis'
    
    def get_queryset(self, request):
        """Otimiza a query incluindo o organizador"""
        qs = super().get_queryset(request)
        return qs.select_related('organizador')


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Inscricao
    """
    list_display = ('get_usuario_nome', 'get_evento_nome', 'data_inscricao', 'ativa', 'data_cancelamento')
    list_filter = ('ativa', 'data_inscricao', 'evento__tipo')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'evento__nome')
    date_hierarchy = 'data_inscricao'
    ordering = ('-data_inscricao',)
    
    fieldsets = (
        ('Inscrição', {
            'fields': ('usuario', 'evento', 'ativa')
        }),
        ('Datas', {
            'fields': ('data_inscricao', 'data_cancelamento'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_inscricao',)
    
    def get_usuario_nome(self, obj):
        """Retorna o nome completo do usuário"""
        return obj.usuario.get_full_name() or obj.usuario.username
    get_usuario_nome.short_description = 'Usuário'
    get_usuario_nome.admin_order_field = 'usuario__first_name'
    
    def get_evento_nome(self, obj):
        """Retorna o nome do evento"""
        return obj.evento.nome
    get_evento_nome.short_description = 'Evento'
    get_evento_nome.admin_order_field = 'evento__nome'
    
    def get_queryset(self, request):
        """Otimiza a query incluindo usuário e evento"""
        qs = super().get_queryset(request)
        return qs.select_related('usuario', 'evento')
    
    actions = ['cancelar_inscricoes', 'reativar_inscricoes']
    
    def cancelar_inscricoes(self, request, queryset):
        """Ação para cancelar inscrições em massa"""
        from django.utils import timezone
        updated = queryset.update(ativa=False, data_cancelamento=timezone.now())
        self.message_user(request, f'{updated} inscrição(ões) cancelada(s) com sucesso.')
    cancelar_inscricoes.short_description = 'Cancelar inscrições selecionadas'
    
    def reativar_inscricoes(self, request, queryset):
        """Ação para reativar inscrições em massa"""
        updated = queryset.update(ativa=True, data_cancelamento=None)
        self.message_user(request, f'{updated} inscrição(ões) reativada(s) com sucesso.')
    reativar_inscricoes.short_description = 'Reativar inscrições selecionadas'


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Certificado
    """
    list_display = ('codigo_verificacao', 'get_usuario_nome', 'get_evento_nome', 'data_emissao', 'emitido_por', 'tem_arquivo')
    list_filter = ('data_emissao', 'inscricao__evento__tipo')
    search_fields = ('codigo_verificacao', 'inscricao__usuario__username', 'inscricao__usuario__first_name', 'inscricao__evento__nome')
    date_hierarchy = 'data_emissao'
    ordering = ('-data_emissao',)
    
    fieldsets = (
        ('Certificado', {
            'fields': ('inscricao', 'codigo_verificacao', 'emitido_por', 'arquivo_pdf')
        }),
        ('Metadados', {
            'fields': ('data_emissao',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('codigo_verificacao', 'data_emissao')
    
    def get_usuario_nome(self, obj):
        """Retorna o nome completo do usuário"""
        return obj.inscricao.usuario.get_full_name() or obj.inscricao.usuario.username
    get_usuario_nome.short_description = 'Participante'
    
    def get_evento_nome(self, obj):
        """Retorna o nome do evento"""
        return obj.inscricao.evento.nome
    get_evento_nome.short_description = 'Evento'
    
    def tem_arquivo(self, obj):
        """Verifica se possui arquivo PDF"""
        return bool(obj.arquivo_pdf)
    tem_arquivo.short_description = 'Arquivo PDF'
    tem_arquivo.boolean = True
    
    def get_queryset(self, request):
        """Otimiza a query incluindo inscrição, usuário e evento"""
        qs = super().get_queryset(request)
        return qs.select_related('inscricao__usuario', 'inscricao__evento', 'emitido_por')
