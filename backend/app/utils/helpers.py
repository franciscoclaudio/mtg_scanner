import os
import re
from PIL import Image
import io

def allowed_file(filename, allowed_extensions):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def clean_filename(filename):
    """Limpa o nome do arquivo para ser seguro"""
    # Remove caracteres não seguros
    cleaned = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return cleaned

def validate_image(file_stream):
    """Valida se o arquivo é uma imagem válida"""
    try:
        image = Image.open(io.BytesIO(file_stream))
        image.verify()  # Verifica se é uma imagem válida
        return True
    except Exception:
        return False

def get_file_extension(filename):
    """Obtém a extensão do arquivo"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
