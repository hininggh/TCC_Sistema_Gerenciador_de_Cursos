import os
from django.core.exceptions import ValidationError

def validate_pdf_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('Este campo aceita apenas arquivos PDF.')