"""
URLs da API REST do SGEA
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import EventoAPIViewSet, InscricaoAPIViewSet

router = DefaultRouter()
router.register(r'eventos', EventoAPIViewSet, basename='api-evento')
router.register(r'inscricoes', InscricaoAPIViewSet, basename='api-inscricao')

urlpatterns = [
    path('auth/login/', obtain_auth_token, name='api-login'),
    path('', include(router.urls)),
]
