"""
Views para o Sistema de Gestão de Eventos Acadêmicos (SGEA)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Usuario, Evento, Inscricao, Certificado
from .forms import UsuarioRegistroForm, EventoForm, LoginForm


# ============================================
# VIEWS DE AUTENTICAÇÃO
# ============================================

def home(request):
    """
    Página inicial do sistema
    """
    eventos_proximos = Evento.objects.filter(
        ativo=True,
        data_inicial__gte=timezone.now().date()
    ).order_by('data_inicial')[:6]
    
    context = {
        'eventos_proximos': eventos_proximos,
        'total_eventos': Evento.objects.filter(ativo=True).count(),
        'total_usuarios': Usuario.objects.count(),
    }
    return render(request, 'eventos/home.html', context)


def registro(request):
    """
    View para cadastro de novos usuários
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                messages.success(
                    request, 
                    'Cadastro realizado com sucesso! Faça login para continuar.'
                )
                return redirect('login')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(
                request, 
                'Por favor, corrija os erros abaixo.'
            )
    else:
        form = UsuarioRegistroForm()
    
    return render(request, 'eventos/registro.html', {'form': form})


def login_view(request):
    """
    View para login de usuários
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.get_full_name()}!')
                
                # Redireciona baseado no perfil
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                messages.error(
                    request, 
                    'Usuário ou senha inválidos.'
                )
    else:
        form = LoginForm()
    
    return render(request, 'eventos/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    View para logout de usuários
    """
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('home')


# ============================================
# VIEWS DO DASHBOARD
# ============================================

@login_required
def dashboard(request):
    """
    Dashboard principal do usuário
    """
    user = request.user
    
    context = {
        'usuario': user,
    }
    
    if user.perfil == 'ORGANIZADOR':
        # Dashboard para organizadores
        eventos = Evento.objects.filter(organizador=user, ativo=True)
        context.update({
            'eventos_organizados': eventos,
            'total_eventos': eventos.count(),
            'total_inscritos': Inscricao.objects.filter(
                evento__organizador=user,
                ativa=True
            ).count(),
            'certificados_emitidos': Certificado.objects.filter(
                emitido_por=user
            ).count(),
        })
        return render(request, 'eventos/dashboard_organizador.html', context)
    
    else:
        # Dashboard para alunos e professores
        inscricoes = Inscricao.objects.filter(
            usuario=user,
            ativa=True
        ).select_related('evento')
        
        context.update({
            'inscricoes_ativas': inscricoes,
            'total_inscricoes': inscricoes.count(),
            'certificados': Certificado.objects.filter(
                inscricao__usuario=user
            ).count(),
        })
        return render(request, 'eventos/dashboard_usuario.html', context)


# ============================================
# VIEWS DE EVENTOS
# ============================================

def eventos_list(request):
    """
    Lista de eventos disponíveis
    """
    eventos = Evento.objects.filter(
        ativo=True
    ).annotate(
        total_inscritos=Count('inscricoes', filter=Q(inscricoes__ativa=True))
    ).order_by('data_inicial')
    
    # Filtro de pesquisa
    search = request.GET.get('search')
    if search:
        eventos = eventos.filter(
            Q(nome__icontains=search) | 
            Q(descricao__icontains=search)
        )
    
    # Filtro de tipo
    tipo = request.GET.get('tipo')
    if tipo:
        eventos = eventos.filter(tipo=tipo)
    
    # Filtro de status
    status = request.GET.get('status')
    if status == 'aberto':
        eventos = eventos.filter(data_inicial__gte=timezone.now().date())
    elif status == 'encerrado':
        eventos = eventos.filter(data_inicial__lt=timezone.now().date())
    
    context = {
        'eventos': eventos,
    }
    return render(request, 'eventos/eventos_list.html', context)


def evento_detail(request, pk):
    """
    Detalhes de um evento específico
    """
    evento = get_object_or_404(Evento, pk=pk, ativo=True)
    
    inscrito = False
    tem_certificado = False
    inscricao = None
    
    if request.user.is_authenticated:
        inscricao = Inscricao.objects.filter(
            usuario=request.user,
            evento=evento,
            ativa=True
        ).first()
        
        inscrito = inscricao is not None
        
        if inscrito:
            tem_certificado = Certificado.objects.filter(
                inscricao__usuario=request.user,
                inscricao__evento=evento
            ).exists()
    
    context = {
        'evento': evento,
        'inscrito': inscrito,
        'inscricao': inscricao,
        'tem_certificado': tem_certificado,
    }
    return render(request, 'eventos/evento_detail.html', context)


@login_required
def evento_create(request):
    """
    Criação de novo evento (apenas organizadores)
    """
    if request.user.perfil != 'ORGANIZADOR':
        messages.error(
            request, 
            'Apenas organizadores podem criar eventos.'
        )
        return redirect('eventos_list')
    
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            try:
                evento.full_clean()
                evento.save()
                messages.success(
                    request, 
                    'Evento criado com sucesso!'
                )
                return redirect('evento_detail', pk=evento.pk)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            messages.error(
                request, 
                'Por favor, corrija os erros no formulário.'
            )
    else:
        form = EventoForm()
    
    return render(request, 'eventos/evento_form.html', {'form': form})


@login_required
def evento_edit(request, pk):
    """
    Edição de evento existente
    """
    evento = get_object_or_404(Evento, pk=pk)
    
    if evento.organizador != request.user:
        messages.error(
            request, 
            'Você não tem permissão para editar este evento.'
        )
        return redirect('evento_detail', pk=pk)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            try:
                evento = form.save(commit=False)
                evento.full_clean()
                evento.save()
                messages.success(
                    request, 
                    'Evento atualizado com sucesso!'
                )
                return redirect('evento_detail', pk=evento.pk)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'eventos/evento_form.html', {
        'form': form,
        'evento': evento,
    })


@login_required
def evento_delete(request, pk):
    """
    Exclusão de evento (apenas organizador responsável)
    """
    evento = get_object_or_404(Evento, pk=pk)
    
    if evento.organizador != request.user:
        messages.error(
            request, 
            'Você não tem permissão para excluir este evento.'
        )
        return redirect('evento_detail', pk=pk)
    
    # Verifica se há inscrições ativas
    inscricoes_ativas = Inscricao.objects.filter(evento=evento, ativa=True).count()
    
    if request.method == 'POST':
        nome_evento = evento.nome
        evento.delete()
        messages.success(
            request, 
            f'Evento "{nome_evento}" excluído com sucesso!'
        )
        return redirect('dashboard')
    
    return render(request, 'eventos/evento_confirm_delete.html', {
        'evento': evento,
        'inscricoes_ativas': inscricoes_ativas,
    })


# ============================================
# VIEWS DE INSCRIÇÕES
# ============================================

@login_required
def inscricao_create(request, evento_pk):
    """
    Inscrição em evento
    """
    evento = get_object_or_404(Evento, pk=evento_pk, ativo=True)
    
    # Verifica se já está inscrito
    inscricao_existente = Inscricao.objects.filter(
        usuario=request.user,
        evento=evento,
        ativa=True
    ).first()
    
    if inscricao_existente:
        messages.warning(
            request, 
            'Você já está inscrito neste evento.'
        )
        return redirect('evento_detail', pk=evento_pk)
    
    # Cria nova inscrição
    inscricao = Inscricao(usuario=request.user, evento=evento)
    
    try:
        inscricao.full_clean()
        inscricao.save()
        messages.success(
            request, 
            f'Inscrição realizada com sucesso no evento "{evento.nome}"!'
        )
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect('evento_detail', pk=evento_pk)


@login_required
def inscricao_cancelar(request, pk):
    """
    Cancelamento de inscrição
    """
    inscricao = get_object_or_404(
        Inscricao, 
        pk=pk, 
        usuario=request.user,
        ativa=True
    )
    
    if request.method == 'POST':
        inscricao.cancelar()
        messages.success(
            request, 
            'Inscrição cancelada com sucesso.'
        )
        return redirect('dashboard')
    
    return render(request, 'eventos/inscricao_cancelar.html', {
        'inscricao': inscricao
    })


@login_required
def minhas_inscricoes(request):
    """
    Lista de inscrições do usuário
    """
    inscricoes = Inscricao.objects.filter(
        usuario=request.user
    ).select_related('evento').order_by('-data_inscricao')
    
    return render(request, 'eventos/minhas_inscricoes.html', {
        'inscricoes': inscricoes
    })


# ============================================
# VIEWS DE CERTIFICADOS
# ============================================

@login_required
def certificado_emitir(request, inscricao_pk):
    """
    Emissão de certificado (apenas organizadores)
    """
    inscricao = get_object_or_404(Inscricao, pk=inscricao_pk)
    
    # Verifica se o usuário é o organizador do evento
    if inscricao.evento.organizador != request.user:
        messages.error(
            request, 
            'Apenas o organizador do evento pode emitir certificados.'
        )
        return redirect('dashboard')
    
    # Verifica se já existe certificado
    if hasattr(inscricao, 'certificado'):
        messages.warning(
            request, 
            'Certificado já foi emitido para este participante.'
        )
        return redirect('evento_inscritos', pk=inscricao.evento.pk)
    
    # Cria certificado
    certificado = Certificado(
        inscricao=inscricao,
        emitido_por=request.user
    )
    
    try:
        certificado.full_clean()
        certificado.save()
        messages.success(
            request, 
            f'Certificado emitido para {inscricao.usuario.get_full_name()}!'
        )
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect('evento_inscritos', pk=inscricao.evento.pk)


@login_required
def evento_inscritos(request, pk):
    """
    Lista de inscritos em um evento (apenas organizador)
    """
    evento = get_object_or_404(Evento, pk=pk)
    
    if evento.organizador != request.user:
        messages.error(
            request, 
            'Você não tem permissão para visualizar os inscritos deste evento.'
        )
        return redirect('dashboard')
    
    inscricoes = Inscricao.objects.filter(
        evento=evento,
        ativa=True
    ).select_related('usuario').prefetch_related('certificado')
    
    return render(request, 'eventos/evento_inscritos.html', {
        'evento': evento,
        'inscricoes': inscricoes,
    })


def certificado_validar(request, codigo=None):
    """Validação de certificado por código"""
    from .models import Auditoria
    
    # Tenta pegar o código da URL ou do query parameter
    if not codigo:
        codigo = request.GET.get('codigo', '')
    
    # Se não há código, mostra o formulário
    if not codigo:
        return render(request, 'eventos/certificado_validar.html')
    
    try:
        certificado = Certificado.objects.get(codigo_verificacao=codigo)
        
        # Registra auditoria
        Auditoria.registrar(
            usuario=request.user if request.user.is_authenticated else None,
            acao='CONSULTAR_CERTIFICADO',
            descricao=f'Consulta de certificado: {codigo}',
            dados_adicionais={
                'codigo': codigo,
                'valido': True
            }
        )
        
        return render(request, 'eventos/certificado_validacao.html', {
            'certificado': certificado,
            'valido': True
        })
    except Certificado.DoesNotExist:
        return render(request, 'eventos/certificado_validacao.html', {
            'valido': False,
            'codigo': codigo
        })


def confirmar_email(request, token):
    """
    Confirma o email do usuário através do token
    """
    try:
        usuario = Usuario.objects.get(token_confirmacao=token)
        
        if not usuario.email_confirmado:
            usuario.email_confirmado = True
            usuario.token_confirmacao = None
            usuario.save(update_fields=['email_confirmado', 'token_confirmacao'])
            
            messages.success(
                request,
                'Email confirmado com sucesso! Você já pode fazer login no sistema.'
            )
        else:
            messages.info(request, 'Este email já foi confirmado anteriormente.')
        
        return redirect('login')
        
    except Usuario.DoesNotExist:
        messages.error(request, 'Token de confirmação inválido.')
        return redirect('home')


@login_required
def auditoria_list(request):
    """
    Lista de registros de auditoria (apenas para organizadores)
    """
    if request.user.perfil != 'ORGANIZADOR':
        messages.error(request, 'Acesso negado. Apenas organizadores podem acessar esta área.')
        return redirect('dashboard')
    
    from .models import Auditoria
    from django.core.paginator import Paginator
    
    # Filtros
    auditorias = Auditoria.objects.all()
    
    # Filtro por data
    data_filtro = request.GET.get('data')
    if data_filtro:
        auditorias = auditorias.filter(data_hora__date=data_filtro)
    
    # Filtro por usuário
    usuario_filtro = request.GET.get('usuario')
    if usuario_filtro:
        auditorias = auditorias.filter(usuario__username__icontains=usuario_filtro)
    
    # Filtro por ação
    acao_filtro = request.GET.get('acao')
    if acao_filtro:
        auditorias = auditorias.filter(acao=acao_filtro)
    
    # Paginação
    paginator = Paginator(auditorias, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'acoes': Auditoria.ACAO_CHOICES,
    }
    
    return render(request, 'eventos/auditoria_list.html', context)

@login_required
def meus_certificados(request):
    """
    Lista de certificados do usuário
    """
    certificados = Certificado.objects.filter(
        inscricao__usuario=request.user
    ).select_related('inscricao__evento')
    
    return render(request, 'eventos/meus_certificados.html', {
        'certificados': certificados
    })


@login_required
def certificado_download(request, pk):
    """
    Download de certificado em PDF
    """
    certificado = get_object_or_404(Certificado, pk=pk)
    
    # Verifica permissão
    if certificado.inscricao.usuario != request.user:
        messages.error(
            request, 
            'Você não tem permissão para baixar este certificado.'
        )
        return redirect('meus_certificados')
    
    # TODO: Implementar geração de PDF
    # Por enquanto, retorna uma resposta simples
    from django.template.loader import render_to_string
    
    html_content = render_to_string('eventos/certificado_pdf.html', {
        'certificado': certificado,
        'inscricao': certificado.inscricao,
        'evento': certificado.inscricao.evento,
        'usuario': certificado.inscricao.usuario,
    })
    
    return HttpResponse(html_content, content_type='text/html')
    # Para produção, usar biblioteca como reportlab ou weasyprint
