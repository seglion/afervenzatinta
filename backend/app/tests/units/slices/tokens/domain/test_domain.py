
import datetime
import uuid
from enum import Enum

from pydantic import BaseModel

from app.slices.tokens.domain.entities import Token  # type: ignore
from app.slices.tokens.domain.values_objects import TokenType  # type: ignore


def test_tokentype_class_exists():

    assert 'TokenType' in globals(), "La clase TokenType no se encontró."

def test_tokentype_inherits_from_enum():

    assert issubclass(TokenType, Enum), "TokenType no hereda de enum.Enum."

def test_tokentype_has_members():

    assert hasattr(TokenType, 'VERIFICATION'), "Falta el atributo 'VERIFICATION'."
    assert hasattr(TokenType, 'PASSWORD_RESET'), "Falta el atributo 'PASSWORD_RESET'."

def test_token_class_exists():

    assert 'Token' in globals(), "La clase Token no se encontró."

def test_token_inherits_from_base_model():
    """
    Verifica que la clase TokenType hereda de enum.Enum.
    Este test fallará hasta que TokenType herede de Enum.
    """
    assert issubclass(Token, BaseModel), "Token no hereda de pydantic.BaseModel."


def test_token_has_members():
    token = Token(token="sample_token",
                  user_id=uuid.uuid4(),
                  token_type=TokenType.VERIFICATION,
                  expired_at=datetime.datetime.now(datetime.timezone.utc),
                  created_at=datetime.datetime.now(datetime.timezone.utc),
    )
    assert isinstance(getattr(token, 'id', None), uuid.UUID), "Esperaba que Token.id fuera uuid.UUID"
    assert isinstance(token.token, str), "Esperaba que Token.token fuera tr"
    assert isinstance(token.user_id, uuid.UUID), "Esperaba que Token.user_id fuera uuid.UUID"
    assert isinstance(token.token_type, TokenType), "Esperaba que Token.token_type fuera TokenType"
    assert isinstance(token.expired_at,datetime.datetime), "Esperaba que Token.expired_at fuera datetime"
    assert isinstance(token.created_at,datetime.datetime), "Esperaba que Token.created_at fuera datetime"
    assert isinstance(token.is_used, bool), "Esperaba que Token.is_used fuera bool"

def test_token_has_method_is_valid():
    """
    Test intencionalmente fallido: verifica que Token implemente el método `is_valid`.
    El test fallará hasta que se añada el método.
    """
    assert callable(getattr(Token, 'is_valid', None)), "Falta el método 'is_valid' en Token."
def test_token_is_valid_returns_bool():
    """
    Test intencionalmente fallido: verifica que Token.is_valid() devuelva un booleano.
    Actualmente Token.is_valid() está sin implementar (retorna None), por lo que este test fallará.
    """
    token = Token(
        token="sample_token",
        user_id=uuid.uuid4(),
        token_type=TokenType.VERIFICATION,
        expired_at=datetime.datetime.now(datetime.timezone.utc),
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )
    result = token.is_valid()
    assert isinstance(result, bool), "Esperaba que Token.is_valid() devolviera un bool"
def test_token_is_valid_matches_expected_logic():
    """
    Comprueba que Token.is_valid() implemente:
    not self.is_used and self.expired_at > datetime.now(timezone.utc)
    (Este test fallará mientras la implementación actual devuelva siempre True.)
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    future = now + datetime.timedelta(hours=1)
    past = now - datetime.timedelta(hours=1)

    # caso válido: no usado y no expirado -> True
    token_ok = Token(
        token="sample_token",
        user_id=uuid.uuid4(),
        token_type=TokenType.VERIFICATION,
        expired_at=future,
        created_at=now,
        is_used=False,
    )
    assert token_ok.is_valid() is True, "Esperaba True cuando no está usado y no ha expirado"

    # caso inválido: ya usado -> False
    token_used = Token(
        token="sample_token",
        user_id=uuid.uuid4(),
        token_type=TokenType.VERIFICATION,
        expired_at=future,
        created_at=now,
        is_used=True,
    )
    assert token_used.is_valid() is False, "Esperaba False cuando is_used es True"

    # caso inválido: expirado -> False
    token_expired = Token(
        token="sample_token",
        user_id=uuid.uuid4(),
        token_type=TokenType.VERIFICATION,
        expired_at=past,
        created_at=now,
        is_used=False,
    )
    assert token_expired.is_valid() is False, "Esperaba False cuando expired_at está en el pasado"
