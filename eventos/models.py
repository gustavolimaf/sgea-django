"""
Models para o Sistema de Gestão de Eventos Acadêmicos (SGEA)
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .validators import validate_phone_number, validate_image_file, validate_future_date


class Usuario(AbstractUser):
    """
    Model customizado de usuário para o SGEA.
    Estende AbstractUser para adicionar campos específicos.
    """
    PERFIL_CHOICES = [
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('ORGANIZADOR', 'Organizador'),
    ]
    
    telefone = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        help_text="Telefone de contato no formato (XX) XXXXX-XXXX"
    )
    
    email_confirmado = models.BooleanField(
        default=False,
        help_text="Indica se o email foi confirmado"
    )
    
    token_confirmacao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Token para confirmação de email"
    )
    
    instituicao = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Instituição de ensino (obrigatório para alunos e professores)"
    )
    
    perfil = models.CharField(
        max_length=12,
        choices=PERFIL_CHOICES,
        default='ALUNO',
        help_text="Perfil do usuário no sistema"
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora do cadastro"
    )
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_perfil_display()})"
    
    def save(self, *args, **kwargs):
        """
        Override do save para validar instituição obrigatória para alunos e professores
        """
        # Não validar para superusuários e staff
        if not self.is_superuser and not self.is_staff:
            if self.perfil in ['ALUNO', 'PROFESSOR'] and not self.instituicao:
                raise ValueError(
                    "Instituição é obrigatória para alunos e professores"
                )
        super().save(*args, **kwargs)


class Evento(models.Model):
    """
    Model para eventos acadêmicos.
    """
    TIPO_CHOICES = [
        ('SEMINARIO', 'Seminário'),
        ('PALESTRA', 'Palestra'),
        ('MINICURSO', 'Minicurso'),
        ('SEMANA_ACADEMICA', 'Semana Acadêmica'),
    ]
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        help_text="Tipo do evento"
    )
    
    nome = models.CharField(
        max_length=200,
        help_text="Nome/título do evento"
    )
    
    descricao = models.TextField(
        help_text="Descrição detalhada do evento"
    )
    
    data_inicial = models.DateField(
        help_text="Data de início do evento"
    )
    
    data_final = models.DateField(
        help_text="Data de término do evento"
    )
    
    horario_inicio = models.TimeField(
        help_text="Horário de início"
    )
    
    horario_fim = models.TimeField(
        help_text="Horário de término"
    )
    
    local = models.CharField(
        max_length=300,
        help_text="Local onde será realizado o evento"
    )
    
    vagas_totais = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantidade máxima de participantes"
    )
    
    organizador = models.ForeignKey(
        'Usuario',
        on_delete=models.PROTECT,
        related_name='eventos_organizados',
        limit_choices_to={'perfil': 'ORGANIZADOR'},
        help_text="Organizador responsável pelo evento"
    )
    
    professor_responsavel = models.ForeignKey(
        'Usuario',
        on_delete=models.PROTECT,
        related_name='eventos_como_responsavel',
        limit_choices_to={'perfil': 'PROFESSOR'},
        null=True,
        blank=True,
        help_text="Professor responsável pelo evento acadêmico"
    )
    
    banner = models.ImageField(
        upload_to='banners/%Y/%m/',
        validators=[validate_image_file],
        null=True,
        blank=True,
        help_text="Banner do evento (JPG, PNG, GIF, WEBP - máx 5MB)"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        help_text="Data de criação do registro"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        help_text="Data da última atualização"
    )
    
    ativo = models.BooleanField(
        default=True,
        help_text="Indica se o evento está ativo"
    )
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-data_inicial', 'horario_inicio']
        indexes = [
            models.Index(fields=['data_inicial']),
            models.Index(fields=['tipo']),
            models.Index(fields=['organizador']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    
    def clean(self):
        """
        Validações customizadas do modelo
        """
        # Validar data inicial futura
        if self.data_inicial:
            validate_future_date(self.data_inicial)
        
        if self.data_final and self.data_inicial:
            if self.data_final < self.data_inicial:
                raise ValidationError({
                    'data_final': 'A data final não pode ser anterior à data inicial.'
                })
        
        if self.horario_fim and self.horario_inicio:
            if self.data_inicial == self.data_final:
                if self.horario_fim <= self.horario_inicio:
                    raise ValidationError({
                        'horario_fim': 'O horário de término deve ser posterior ao horário de início.'
                    })
        
        # Validar professor responsável
        if self.professor_responsavel and self.professor_responsavel.perfil != 'PROFESSOR':
            raise ValidationError({
                'professor_responsavel': 'O responsável deve ser um professor.'
            })
    
    @property
    def vagas_disponiveis(self):
        """
        Retorna o número de vagas disponíveis
        """
        inscritos = self.inscricoes.filter(ativa=True).count()
        return self.vagas_totais - inscritos
    
    @property
    def esta_lotado(self):
        """
        Verifica se o evento está lotado
        """
        return self.vagas_disponiveis <= 0
    
    @property
    def ja_ocorreu(self):
        """
        Verifica se o evento já ocorreu
        """
        hoje = timezone.now().date()
        return self.data_final < hoje


class Inscricao(models.Model):
    """
    Model para inscrições de usuários em eventos.
    """
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='inscricoes',
        help_text="Usuário inscrito"
    )
    
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='inscricoes',
        help_text="Evento em que o usuário está inscrito"
    )
    
    data_inscricao = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora da inscrição"
    )
    
    ativa = models.BooleanField(
        default=True,
        help_text="Indica se a inscrição está ativa"
    )
    
    data_cancelamento = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data e hora do cancelamento (se aplicável)"
    )
    
    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        ordering = ['-data_inscricao']
        unique_together = ['usuario', 'evento']
        indexes = [
            models.Index(fields=['usuario', 'ativa']),
            models.Index(fields=['evento', 'ativa']),
        ]
    
    def __str__(self):
        status = "Ativa" if self.ativa else "Cancelada"
        return f"{self.usuario.get_full_name()} - {self.evento.nome} ({status})"
    
    def clean(self):
        """
        Validações customizadas
        """
        # Verifica se o evento já ocorreu
        if self.evento.ja_ocorreu:
            raise ValidationError(
                'Não é possível se inscrever em eventos que já ocorreram.'
            )
        
        # Verifica se há vagas disponíveis (apenas para novas inscrições)
        if not self.pk and self.evento.esta_lotado:
            raise ValidationError(
                'Este evento não possui mais vagas disponíveis.'
            )
        
        # Verifica se usuário é organizador (organizadores não podem se inscrever)
        if self.usuario.perfil == 'ORGANIZADOR':
            raise ValidationError(
                'Organizadores não podem se inscrever em eventos.'
            )
        
        # Verifica duplicidade de inscrição
        if not self.pk:
            inscricao_existente = Inscricao.objects.filter(
                usuario=self.usuario,
                evento=self.evento,
                ativa=True
            ).exists()
            
            if inscricao_existente:
                raise ValidationError(
                    'Você já está inscrito neste evento.'
                )
    
    def cancelar(self):
        """
        Cancela a inscrição
        """
        self.ativa = False
        self.data_cancelamento = timezone.now()
        self.save()


class Certificado(models.Model):
    """
    Model para certificados emitidos aos participantes.
    """
    inscricao = models.OneToOneField(
        Inscricao,
        on_delete=models.CASCADE,
        related_name='certificado',
        help_text="Inscrição vinculada ao certificado"
    )
    
    codigo_verificacao = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único para verificação do certificado"
    )
    
    data_emissao = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora da emissão do certificado"
    )
    
    emitido_por = models.ForeignKey(
        'Usuario',
        on_delete=models.PROTECT,
        related_name='certificados_emitidos',
        help_text="Organizador que emitiu o certificado"
    )
    
    arquivo_pdf = models.FileField(
        upload_to='certificados/%Y/%m/',
        null=True,
        blank=True,
        help_text="Arquivo PDF do certificado"
    )
    
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        ordering = ['-data_emissao']
        indexes = [
            models.Index(fields=['codigo_verificacao']),
        ]
    
    def __str__(self):
        return f"Certificado #{self.codigo_verificacao} - {self.inscricao.usuario.get_full_name()}"
    
    def save(self, *args, **kwargs):
        """
        Gera código de verificação único se não existir
        """
        if not self.codigo_verificacao:
            import uuid
            self.codigo_verificacao = str(uuid.uuid4())[:50]
        super().save(*args, **kwargs)
    
    def clean(self):
        """
        Validações customizadas
        """
        # Verifica se a inscrição está ativa
        if not self.inscricao.ativa:
            raise ValidationError(
                'Não é possível emitir certificado para inscrição cancelada.'
            )
        
        # Verifica se o emissor é organizador do evento
        if self.emitido_por != self.inscricao.evento.organizador:
            raise ValidationError(
                'Apenas o organizador do evento pode emitir certificados.'
            )


class Auditoria(models.Model):
    """
    Model para registro de auditoria (logs) das ações do sistema.
    """
    ACAO_CHOICES = [
        ('CRIAR_USUARIO', 'Criação de usuário'),
        ('CRIAR_EVENTO', 'Cadastro de evento'),
        ('EDITAR_EVENTO', 'Alteração de evento'),
        ('EXCLUIR_EVENTO', 'Exclusão de evento'),
        ('INSCRICAO', 'Inscrição em evento'),
        ('CANCELAR_INSCRICAO', 'Cancelamento de inscrição'),
        ('EMITIR_CERTIFICADO', 'Emissão de certificado'),
        ('CONSULTAR_CERTIFICADO', 'Consulta de certificado'),
        ('API_CONSULTA', 'Consulta via API'),
        ('API_INSCRICAO', 'Inscrição via API'),
    ]
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='acoes_auditoria',
        help_text="Usuário que realizou a ação"
    )
    
    acao = models.CharField(
        max_length=30,
        choices=ACAO_CHOICES,
        help_text="Tipo de ação realizada"
    )
    
    descricao = models.TextField(
        help_text="Descrição detalhada da ação"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Endereço IP de origem"
    )
    
    data_hora = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora da ação"
    )
    
    dados_adicionais = models.JSONField(
        null=True,
        blank=True,
        help_text="Dados adicionais sobre a ação (JSON)"
    )
    
    class Meta:
        verbose_name = "Auditoria"
        verbose_name_plural = "Auditorias"
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['usuario', 'data_hora']),
            models.Index(fields=['acao', 'data_hora']),
            models.Index(fields=['data_hora']),
        ]
    
    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Sistema"
        return f"{usuario_str} - {self.get_acao_display()} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
    
    @staticmethod
    def registrar(usuario, acao, descricao, ip_address=None, dados_adicionais=None):
        """
        Método auxiliar para registrar uma ação de auditoria
        """
        return Auditoria.objects.create(
            usuario=usuario,
            acao=acao,
            descricao=descricao,
            ip_address=ip_address,
            dados_adicionais=dados_adicionais
        )
