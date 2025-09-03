import datetime
import hashlib
import secrets
from typing import Tuple


def generate_secure_token_pair() -> Tuple[str, str]:
    """
     Genera un token crudo seguro para la URL y su correspondiente hash SHA-256.

    Returns:
        Una tupla conteniendo (raw_token, hashed_token).
    """

    # Paso 1: Generar un token de 32 bytes, seguro a nivel criptográfico
    # y codificado en base64 para ser seguro en URLs.
    raw_token = secrets.token_urlsafe(32)
    # Paso 2: Hashear el token para un almacenamiento seguro en la BD.
    # Se usa SHA-256, que es un estándar rápido y seguro para este fin.
    # No se necesita un hash lento (como Argon2) porque el token ya es aleatorio
    # y de alta entropía, a diferencia de una contraseña elegida por un humano.
    hashed_token = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    return raw_token, hashed_token  # Placeholder for the actual implementation of


def calculate_expiry_date(minutes: int) -> datetime.datetime:
    if minutes < 0:
        raise ValueError("El parámetro 'minutes' no puede ser negativo.")
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=minutes
    )
