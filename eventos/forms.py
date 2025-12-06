"""
Forms para o Sistema de Gestão de Eventos Acadêmicos (SGEA)
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Evento
from .validators import validate_strong_password


class UsuarioRegistroForm(UserCreationForm):
    """
    Formulário de registro de novos usuários
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999',
            'data-mask': '(00) 00000-0000'
        }),
        help_text='Formato: (XX) XXXXX-XXXX'
    )
    
    instituicao = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da instituição'
        })
    )
    
    perfil = forms.ChoiceField(
        choices=Usuario.PERFIL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'telefone', 'instituicao', 'perfil', 
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escolha um nome de usuário'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
        self.fields['password1'].help_text = 'Mínimo 8 caracteres, letras, números e caracteres especiais'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            validate_strong_password(password)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        perfil = cleaned_data.get('perfil')
        instituicao = cleaned_data.get('instituicao')
        
        # Validar instituição obrigatória para alunos e professores
        if perfil in ['ALUNO', 'PROFESSOR'] and not instituicao:
            raise ValidationError({
                'instituicao': 'Instituição é obrigatória para alunos e professores.'
            })
        
        return cleaned_data


class LoginForm(forms.Form):
    """
    Formulário de login
    """
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class EventoForm(forms.ModelForm):
    """
    Formulário para criação e edição de eventos
    """
    data_inicial = forms.DateField(
        label='Data Inicial',
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'type': 'date'
        })
    )
    
    data_final = forms.DateField(
        label='Data Final',
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker',
            'type': 'date'
        })
    )
    
    horario_inicio = forms.TimeField(
        label='Horário de Início',
        widget=forms.TimeInput(attrs={
            'class': 'form-control timepicker',
            'type': 'time'
        })
    )
    
    horario_fim = forms.TimeField(
        label='Horário de Término',
        widget=forms.TimeInput(attrs={
            'class': 'form-control timepicker',
            'type': 'time'
        })
    )
    
    professor_responsavel = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(perfil='PROFESSOR'),
        label='Professor Responsável',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Selecione o professor responsável pelo evento'
    )
    
    banner = forms.ImageField(
        label='Banner do Evento',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Imagem do evento (JPG, PNG, GIF, WEBP - máx 5MB)'
    )
    
    class Meta:
        model = Evento
        fields = [
            'tipo', 'nome', 'descricao', 
            'data_inicial', 'data_final', 
            'horario_inicio', 'horario_fim',
            'local', 'vagas_totais', 'professor_responsavel',
            'banner', 'ativo'
        ]
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Workshop de Python para Iniciantes'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva o evento, seus objetivos e o que será abordado...'
            }),
            'local': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Auditório Principal - Bloco 1'
            }),
            'vagas_totais': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '50'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
