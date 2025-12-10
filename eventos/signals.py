"""
Signals para o Sistema de Gestão de Eventos Acadêmicos (SGEA)
"""
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import Usuario, Evento, Inscricao, Certificado, Auditoria


@receiver(post_save, sender=Usuario)
def usuario_post_save(sender, instance, created, **kwargs):
    """
    Signal executado após salvar um usuário
    """
    if created:
        # Gera token de confirmação
        instance.token_confirmacao = str(uuid.uuid4())
        instance.save(update_fields=['token_confirmacao'])
        
        # Registra auditoria
        Auditoria.registrar(
            usuario=instance,
            acao='CRIAR_USUARIO',
            descricao=f'Novo usuário cadastrado: {instance.username} ({instance.get_perfil_display()})',
            dados_adicionais={
                'perfil': instance.perfil,
                'email': instance.email
            }
        )
        
        # Envia email de boas-vindas
        enviar_email_boas_vindas(instance)


@receiver(post_save, sender=Evento)
def evento_post_save(sender, instance, created, **kwargs):
    """
    Signal executado após salvar um evento
    """
    if created:
        # Registra auditoria
        Auditoria.registrar(
            usuario=instance.organizador,
            acao='CRIAR_EVENTO',
            descricao=f'Evento criado: {instance.nome}',
            dados_adicionais={
                'evento_id': instance.id,
                'tipo': instance.tipo,
                'data_inicial': str(instance.data_inicial)
            }
        )
    else:
        # Registra auditoria de edição
        Auditoria.registrar(
            usuario=instance.organizador,
            acao='EDITAR_EVENTO',
            descricao=f'Evento editado: {instance.nome}',
            dados_adicionais={
                'evento_id': instance.id,
                'tipo': instance.tipo
            }
        )


@receiver(post_delete, sender=Evento)
def evento_post_delete(sender, instance, **kwargs):
    """
    Signal executado após deletar um evento
    """
    Auditoria.registrar(
        usuario=instance.organizador,
        acao='EXCLUIR_EVENTO',
        descricao=f'Evento excluído: {instance.nome}',
        dados_adicionais={
            'evento_id': instance.id,
            'tipo': instance.tipo
        }
    )


@receiver(post_save, sender=Inscricao)
def inscricao_post_save(sender, instance, created, **kwargs):
    """
    Signal executado após salvar uma inscrição
    """
    if created:
        # Registra auditoria
        Auditoria.registrar(
            usuario=instance.usuario,
            acao='INSCRICAO',
            descricao=f'Inscrição realizada no evento: {instance.evento.nome}',
            dados_adicionais={
                'evento_id': instance.evento.id,
                'evento_nome': instance.evento.nome
            }
        )
        
        # Envia email de confirmação de inscrição
        enviar_email_confirmacao_inscricao(instance)
    elif not instance.ativa and instance.data_cancelamento:
        # Registra auditoria de cancelamento
        Auditoria.registrar(
            usuario=instance.usuario,
            acao='CANCELAR_INSCRICAO',
            descricao=f'Inscrição cancelada no evento: {instance.evento.nome}',
            dados_adicionais={
                'evento_id': instance.evento.id,
                'evento_nome': instance.evento.nome
            }
        )


@receiver(post_save, sender=Certificado)
def certificado_post_save(sender, instance, created, **kwargs):
    """
    Signal executado após salvar um certificado
    """
    if created:
        # Registra auditoria
        Auditoria.registrar(
            usuario=instance.emitido_por,
            acao='EMITIR_CERTIFICADO',
            descricao=f'Certificado emitido para {instance.inscricao.usuario.get_full_name()}',
            dados_adicionais={
                'certificado_id': instance.id,
                'codigo': instance.codigo_verificacao,
                'evento': instance.inscricao.evento.nome
            }
        )


def enviar_email_boas_vindas(usuario):
    """
    Envia email de boas-vindas com link de confirmação
    """
    try:
        from django.core.mail import EmailMultiAlternatives
        import os
        
        assunto = 'Bem-vindo ao SGEA - Confirme seu email'
        
        # Link de confirmação
        link_confirmacao = f"{settings.SITE_URL}/confirmar-email/{usuario.token_confirmacao}/"
        
        contexto = {
            'nome': usuario.get_full_name(),
            'username': usuario.username,
            'link_confirmacao': link_confirmacao,
            'perfil': usuario.get_perfil_display()
        }
        
        mensagem_html = render_to_string('eventos/emails/boas_vindas.html', contexto)
        mensagem_texto = render_to_string('eventos/emails/boas_vindas.txt', contexto)
        
        # Criar email com anexo inline
        email = EmailMultiAlternatives(
            assunto,
            mensagem_texto,
            settings.DEFAULT_FROM_EMAIL,
            [usuario.email]
        )
        email.attach_alternative(mensagem_html, "text/html")
        
        # Anexar logo como inline
        logo_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'images/favicon_io/android-chrome-512x512.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                email.attach('logo.png', f.read(), 'image/png')
                email.content_subtype = 'html'
        
        email.send(fail_silently=True)
    except Exception as e:
        print(f"Erro ao enviar email de boas-vindas: {e}")


def enviar_email_confirmacao_inscricao(inscricao):
    """
    Envia email de confirmação de inscrição
    """
    try:
        from django.core.mail import EmailMultiAlternatives
        import os
        
        assunto = f'Inscrição confirmada - {inscricao.evento.nome}'
        
        contexto = {
            'nome': inscricao.usuario.get_full_name(),
            'evento': inscricao.evento
        }
        
        mensagem_html = render_to_string('eventos/emails/confirmacao_inscricao.html', contexto)
        mensagem_texto = render_to_string('eventos/emails/confirmacao_inscricao.txt', contexto)
        
        # Criar email com anexo inline
        email = EmailMultiAlternatives(
            assunto,
            mensagem_texto,
            settings.DEFAULT_FROM_EMAIL,
            [inscricao.usuario.email]
        )
        email.attach_alternative(mensagem_html, "text/html")
        
        # Anexar logo como inline
        logo_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'images/favicon_io/android-chrome-512x512.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                email.attach('logo.png', f.read(), 'image/png')
                email.content_subtype = 'html'
        
        email.send(fail_silently=True)
    except Exception as e:
        print(f"Erro ao enviar email de confirmação: {e}")


def gerar_certificados_automaticos():
    """
    Função para gerar certificados automáticos após o término dos eventos.
    Deve ser executada por um cron job ou task scheduler.
    """
    from datetime import date
    
    # Busca eventos que terminaram ontem
    ontem = date.today() - timezone.timedelta(days=1)
    eventos_finalizados = Evento.objects.filter(
        data_final=ontem,
        ativo=True
    )
    
    certificados_gerados = 0
    
    for evento in eventos_finalizados:
        # Busca inscrições ativas do evento
        inscricoes = Inscricao.objects.filter(
            evento=evento,
            ativa=True
        ).exclude(certificado__isnull=False)
        
        for inscricao in inscricoes:
            try:
                # Cria certificado
                Certificado.objects.create(
                    inscricao=inscricao,
                    emitido_por=evento.organizador
                )
                certificados_gerados += 1
            except Exception as e:
                print(f"Erro ao gerar certificado para {inscricao}: {e}")
    
    return certificados_gerados
