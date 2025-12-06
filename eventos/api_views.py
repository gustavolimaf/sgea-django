"""
Views da API REST do SGEA
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Evento, Inscricao, Auditoria
from .serializers import (
    EventoListSerializer, EventoDetailSerializer,
    InscricaoCreateSerializer, InscricaoListSerializer
)
from .throttles import EventosListThrottle, InscricoesCreateThrottle


def get_client_ip(request):
    """
    Obtém o endereço IP do cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class EventoAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet para consulta de eventos
    
    list: Lista todos os eventos ativos e futuros
    retrieve: Detalhes de um evento específico
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [EventosListThrottle]
    
    def get_queryset(self):
        """
        Retorna apenas eventos ativos e futuros
        """
        return Evento.objects.filter(
            ativo=True,
            data_inicial__gte=timezone.now().date()
        ).select_related('organizador', 'professor_responsavel')
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado
        """
        if self.action == 'retrieve':
            return EventoDetailSerializer
        return EventoListSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Lista eventos com registro de auditoria
        """
        response = super().list(request, *args, **kwargs)
        
        # Registra auditoria
        Auditoria.registrar(
            usuario=request.user,
            acao='API_CONSULTA',
            descricao=f'Consulta de eventos via API',
            ip_address=get_client_ip(request),
            dados_adicionais={
                'total_resultados': len(response.data.get('results', []))
            }
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """
        Detalhes de evento com registro de auditoria
        """
        response = super().retrieve(request, *args, **kwargs)
        
        # Registra auditoria
        Auditoria.registrar(
            usuario=request.user,
            acao='API_CONSULTA',
            descricao=f'Consulta de evento #{kwargs.get("pk")} via API',
            ip_address=get_client_ip(request),
            dados_adicionais={
                'evento_id': kwargs.get('pk')
            }
        )
        
        return response


class InscricaoAPIViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para inscrições em eventos
    
    list: Lista as inscrições do usuário autenticado
    create: Cria uma nova inscrição
    destroy: Cancela uma inscrição
    """
    permission_classes = [IsAuthenticated]
    serializer_class = InscricaoListSerializer
    
    def get_queryset(self):
        """
        Retorna apenas as inscrições do usuário autenticado
        """
        return Inscricao.objects.filter(
            usuario=self.request.user,
            ativa=True
        ).select_related('evento', 'usuario')
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado
        """
        if self.action == 'create':
            return InscricaoCreateSerializer
        return InscricaoListSerializer
    
    def get_throttles(self):
        """
        Aplica throttle apenas para criação de inscrições
        """
        if self.action == 'create':
            return [InscricoesCreateThrottle()]
        return []
    
    def create(self, request, *args, **kwargs):
        """
        Cria uma nova inscrição com registro de auditoria
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Registra auditoria
        inscricao = serializer.instance
        Auditoria.registrar(
            usuario=request.user,
            acao='API_INSCRICAO',
            descricao=f'Inscrição via API no evento: {inscricao.evento.nome}',
            ip_address=get_client_ip(request),
            dados_adicionais={
                'evento_id': inscricao.evento.id,
                'inscricao_id': inscricao.id
            }
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            InscricaoListSerializer(inscricao).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Cancela uma inscrição
        """
        inscricao = self.get_object()
        
        # Verifica se pode cancelar
        if inscricao.evento.ja_ocorreu:
            return Response(
                {'detail': 'Não é possível cancelar inscrição de evento que já ocorreu.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancela a inscrição
        inscricao.cancelar()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
