"""
Serializers para a API REST do SGEA
"""
from rest_framework import serializers
from .models import Evento, Inscricao, Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para informações básicas do usuário
    """
    nome_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nome_completo', 'perfil']
    
    def get_nome_completo(self, obj):
        return obj.get_full_name()


class EventoListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de eventos
    """
    organizador_nome = serializers.CharField(source='organizador.get_full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    vagas_disponiveis = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Evento
        fields = [
            'id', 'nome', 'tipo', 'tipo_display', 
            'data_inicial', 'data_final', 'horario_inicio', 'horario_fim',
            'local', 'vagas_totais', 'vagas_disponiveis',
            'organizador_nome'
        ]


class EventoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes de um evento específico
    """
    organizador = UsuarioSerializer(read_only=True)
    professor_responsavel = UsuarioSerializer(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    vagas_disponiveis = serializers.IntegerField(read_only=True)
    total_inscritos = serializers.SerializerMethodField()
    
    class Meta:
        model = Evento
        fields = [
            'id', 'tipo', 'tipo_display', 'nome', 'descricao',
            'data_inicial', 'data_final', 'horario_inicio', 'horario_fim',
            'local', 'vagas_totais', 'vagas_disponiveis', 'total_inscritos',
            'organizador', 'professor_responsavel', 'banner'
        ]
    
    def get_total_inscritos(self, obj):
        return obj.inscricoes.filter(ativa=True).count()


class InscricaoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar inscrições via API
    """
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Inscricao
        fields = ['evento', 'usuario']
    
    def validate(self, data):
        """
        Validações personalizadas
        """
        evento = data.get('evento')
        usuario = data.get('usuario')
        
        # Verifica se é organizador
        if usuario.perfil == 'ORGANIZADOR':
            raise serializers.ValidationError(
                'Organizadores não podem se inscrever em eventos.'
            )
        
        # Verifica vagas
        if evento.esta_lotado:
            raise serializers.ValidationError(
                'Este evento não possui mais vagas disponíveis.'
            )
        
        # Verifica duplicidade
        if Inscricao.objects.filter(usuario=usuario, evento=evento, ativa=True).exists():
            raise serializers.ValidationError(
                'Você já está inscrito neste evento.'
            )
        
        # Verifica se evento já ocorreu
        if evento.ja_ocorreu:
            raise serializers.ValidationError(
                'Não é possível se inscrever em eventos que já ocorreram.'
            )
        
        return data


class InscricaoListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de inscrições
    """
    evento = EventoListSerializer(read_only=True)
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Inscricao
        fields = ['id', 'evento', 'usuario', 'data_inscricao', 'ativa']
