"""
Throttle personalizados para a API REST do SGEA
"""
from rest_framework.throttling import UserRateThrottle


class EventosListThrottle(UserRateThrottle):
    """
    Throttle para consulta de eventos: 20 requisições por dia
    """
    rate = '20/day'


class InscricoesCreateThrottle(UserRateThrottle):
    """
    Throttle para inscrições: 50 requisições por dia
    """
    rate = '50/day'
