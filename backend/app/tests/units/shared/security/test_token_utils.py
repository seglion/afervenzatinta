# Tests para las utilidades de tokens en app.shared.security.token_utils
# Cada test incluye comentarios inline que aclaran su propósito y qué comprueba.

import datetime  # usado para crear y comparar datetimes con timezone
import hashlib  # usado para comprobar el hash SHA-256
from inspect import signature  # usado para inspeccionar parámetros y anotaciones de funciones
import pytest
from typing import Tuple  # usado para comparar anotaciones de retorno

# Importar las funciones a probar desde el módulo de utilidades.
# Aquí importamos explícitamente las dos funciones que se testean en este archivo.
from app.shared.security.token_utils import (
    generate_secure_token_pair,
    calculate_expiry_date,
)


# ---------- Existence ----------
# Comprobaciones de existencia de las funciones exportadas por token_utils.py

def test_generate_secure_token_pair_function_exists():
    # Verifica que la función generate_secure_token_pair esté presente en globals()
    assert (
        'generate_secure_token_pair' in globals()
    ), 'La función generate_secure_token_pair no se encontró.'


def test_calculate_expiry_date_function_exists():
    # Verifica que la función calculate_expiry_date esté presente en globals()
    assert (
        'calculate_expiry_date' in globals()
    ), 'La función calculate_expiry_date no se encontró.'


def test_calculate_expiry_date_parameters():
    # Comprueba la firma: debe aceptar un parámetro 'minutes'
    func = globals().get('calculate_expiry_date', None)

    params = list(signature(func).parameters.keys())
    assert "minutes" in params, f'Se esperaba un parámetro "minutes", pero se encontraron: {params}'

    # Comprueba la anotación del parámetro 'minutes' (debe ser int).
    # signature(func).parameters["minutes"].annotation devuelve la anotación tal cual.
    hints = signature(func).parameters["minutes"].annotation
    assert hints == int, f'Se esperaba que el parámetro "minutes" fuera de tipo int, pero se encontró: {hints!r}'


def test_calculate_expiry_date_return_type():
    # Comprueba que la anotación de retorno sea datetime.datetime
    func = globals().get('calculate_expiry_date', None)
    ret = signature(func).return_annotation
    assert ret == datetime.datetime, f'Se esperaba que el tipo de retorno fuera datetime.datetime, pero se encontró: {ret!r}'


def test_calculate_expiry_date_correctness():
    # Valida la lógica: ahora + minutes ≈ resultado de calculate_expiry_date(minutes)
    minutes = 30
    now = datetime.datetime.now(datetime.timezone.utc)  # datetime aware en UTC
    expected = now + datetime.timedelta(minutes=minutes)
    result = calculate_expiry_date(minutes)
    # Permitir una pequeña tolerancia (p. ej. diferencias por ejecución)
    delta = abs((result - expected).total_seconds())
    assert delta < 2, f'Se esperaba que la fecha de expiración fuera aproximadamente {expected}, pero se encontró {result}. Diferencia en segundos: {delta}'


# test para comprobar que el parametro minutos no puede ser negativo, y muestra un error de valor
def test_calculate_expiry_date_negative_minutes():
    # Si minutes < 0, la función debe lanzar ValueError
    with pytest.raises(ValueError):
        calculate_expiry_date(-10)


def test_generate_secure_token_pair_parameters():
    # Comprueba que generate_secure_token_pair no acepte parámetros (firma sin params)
    func = globals().get('generate_secure_token_pair', None)
    params = list(signature(func).parameters.keys())

    assert params == [], f'Se esperaban 0 parámetros, pero se encontraron: {params}'


def test_generate_secure_token_pair_return_type():
    # Comprueba la anotación de retorno: Tuple[str, str]
    func = globals().get('generate_secure_token_pair', None)
    ret = signature(func).return_annotation
    assert (
        ret == Tuple[str, str]
    ), f"Se esperaba que el tipo de retorno fuera 'Tuple[str, str]', pero se encontró: {ret!r}"


def test_generate_secure_token_pair_returns_tuple_of_two_strings():
    # Verifica el tipo en tiempo de ejecución: tupla de 2 strings
    token_pair = generate_secure_token_pair()
    assert isinstance(token_pair, tuple), 'Se esperaba que el retorno fuera una tupla.'
    assert (
        len(token_pair) == 2
    ), f'Se esperaban 2 elementos en la tupla, pero se encontraron {len(token_pair)}.'
    assert all(
        isinstance(t, str) for t in token_pair
    ), 'Se esperaba que ambos elementos de la tupla fueran cadenas de texto (str).'


def test_generate_secure_token_pair_tokens_are_different():
    # Cada llamada debe producir tokens distintos
    token1, token2 = generate_secure_token_pair()
    assert token1 != token2, 'Se esperaban dos tokens diferentes, pero son iguales.'


def test_generate_secure_token_pair_tokens_are_non_empty():
    # Tokens no deben ser cadenas vacías
    token1, token2 = generate_secure_token_pair()
    assert token1, 'El primer token es una cadena vacía.'
    assert token2, 'El segundo token es una cadena vacía.'


def test_generate_secure_token_first_token_32bits_length():
    # Comprobación mínima de longitud para el primer token (al menos 32 chars)
    token1, token2 = generate_secure_token_pair()
    assert (
        len(token1) >= 32
    ), f'Se esperaba que el primer token tuviera al menos 32 caracteres, pero tiene {len(token1)}.'


def test_generate_secure_token_first_token_is_aleatory():
    # Asegura aleatoriedad entre llamadas: primer token cambia
    token1, token2 = generate_secure_token_pair()
    token3, token4 = generate_secure_token_pair()
    assert token1 != token3, 'Se esperaban tokens aleatorios, pero son iguales.'


def test_generate_secure_token_second_token_is_aleatory():
    # Asegura aleatoriedad entre llamadas: segundo token cambia
    token1, token2 = generate_secure_token_pair()
    token3, token4 = generate_secure_token_pair()
    assert token2 != token4, 'Se esperaban tokens aleatorios, pero son iguales.'


def test_generate_secure_token_pair_are_alphanumeric():
    # Primer token: permitir alfanumérico o incluir - o _
    # Segundo token: debe ser un hash hexadecimal (solo caracteres 0-9a-f)
    token1, token2 = generate_secure_token_pair()
    assert (
        token1.isalnum() or ('-' in token1) or ('_' in token1)
    ), 'El primer token debe ser alfanumérico o contener - o _.'
    assert all(
        c in '0123456789abcdef' for c in token2
    ), 'El segundo token debe ser un hash hexadecimal.'


def test_generate_secure_token_pair_second_token_is_sha256_of_first():
    # Comprueba que el segundo token sea el SHA-256 del primero (hexdigest)
    token1, token2 = generate_secure_token_pair()
    expected_hash = hashlib.sha256(token1.encode('utf-8')).hexdigest()
    assert (
        token2 == expected_hash
    ), 'El segundo token debe ser el hash SHA-256 del primer token.'
