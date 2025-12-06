"""
Validators personalizados para o SGEA
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_strong_password(value):
    """
    Valida se a senha atende aos requisitos de segurança:
    - Mínimo 8 caracteres
    - Letras
    - Números
    - Caracteres especiais
    """
    if len(value) < 8:
        raise ValidationError(
            _('A senha deve ter no mínimo 8 caracteres.'),
            code='password_too_short'
        )
    
    if not re.search(r'[a-zA-Z]', value):
        raise ValidationError(
            _('A senha deve conter pelo menos uma letra.'),
            code='password_no_letter'
        )
    
    if not re.search(r'\d', value):
        raise ValidationError(
            _('A senha deve conter pelo menos um número.'),
            code='password_no_number'
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(
            _('A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>).'),
            code='password_no_special'
        )


def validate_image_file(value):
    """
    Valida se o arquivo é uma imagem válida
    """
    import os
    from django.core.files.images import get_image_dimensions
    
    # Verifica extensão
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    if ext not in valid_extensions:
        raise ValidationError(
            _('Apenas arquivos de imagem são permitidos (JPG, PNG, GIF, WEBP).'),
            code='invalid_image_extension'
        )
    
    # Verifica se é realmente uma imagem
    try:
        w, h = get_image_dimensions(value)
        if w is None or h is None:
            raise ValidationError(
                _('O arquivo enviado não é uma imagem válida.'),
                code='invalid_image'
            )
    except Exception:
        raise ValidationError(
            _('O arquivo enviado não é uma imagem válida.'),
            code='invalid_image'
        )
    
    # Verifica tamanho (max 5MB)
    if value.size > 5 * 1024 * 1024:
        raise ValidationError(
            _('A imagem deve ter no máximo 5MB.'),
            code='image_too_large'
        )


def validate_phone_number(value):
    """
    Valida o formato do telefone brasileiro
    Formatos aceitos: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    """
    # Remove caracteres não numéricos
    phone = re.sub(r'\D', '', value)
    
    # Verifica se tem 10 ou 11 dígitos
    if len(phone) not in [10, 11]:
        raise ValidationError(
            _('Telefone deve ter 10 ou 11 dígitos (DDD + número).'),
            code='invalid_phone_length'
        )
    
    # Verifica formato com máscara
    pattern = r'^\(\d{2}\)\s?\d{4,5}-\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX.'),
            code='invalid_phone_format'
        )


def validate_future_date(value):
    """
    Valida se a data é futura (não permite datas passadas)
    """
    from django.utils import timezone
    
    if value < timezone.now().date():
        raise ValidationError(
            _('A data não pode ser anterior à data atual.'),
            code='past_date'
        )
