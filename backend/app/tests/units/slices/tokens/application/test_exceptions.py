

from app.slices.tokens.application.exceptions import (  # type: ignore
    ExpiredTokenException,
    InvalidTokenException,
    TokenException,
)


def test_tokenexception_exists():
    assert 'TokenException' in globals(), "La clase 'TokenException' no está definida."


def test_tokenexception_inherits_from_exception():
    assert issubclass(
        TokenException, Exception
    ), 'TokenException no hereda de Exception.'


def test_invalidtokenexception_exists():
    assert (
        'InvalidTokenException' in globals()
    ), "La clase 'InvalidTokenException' no está definida."


def test_tokenexception_inherits_from_tokenexception():
    assert issubclass(
        InvalidTokenException, TokenException
    ), 'InvalidTokenException no hereda de TokenException.'


def test_expiredtokenexception_exists():
    assert (
        'ExpiredTokenException' in globals()
    ), "La clase 'ExpiredTokenError' no está definida."


def test_expiredexception_inherits_from_tokenexception():
    assert issubclass(
        ExpiredTokenException, TokenException
    ), 'ExpiredTokenException no hereda de TokenException.'
