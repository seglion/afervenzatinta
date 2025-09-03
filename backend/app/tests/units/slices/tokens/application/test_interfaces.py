import datetime
import sys
import uuid
from abc import ABC
from inspect import signature
from typing import Optional, get_type_hints

import pytest

from app.slices.tokens.domain.entities import Token
from app.slices.tokens.domain.values_objects import TokenType
from app.slices.tokens.application.interfaces import ITokenRepository

# ---------- Helpers ----------
def _hints(func):
    return get_type_hints(func, vars(sys.modules[ITokenRepository.__module__]))


# ---------- Existence & ABC ----------
def test_i_token_repository_interface_exists():
    assert 'ITokenRepository' in globals(), 'La clase ITokenRepository no se encontró.'


def test_i_token_repository_inherits_from_abc():
    assert issubclass(ITokenRepository, ABC), 'ITokenRepository no hereda de ABC'


@pytest.mark.parametrize(
    'method_name',
    [
        'create',
        'get_by_token',
        'mark_as_used',
        'deleted',
        'delete_by_user_and_type',
        'find_active_by_user_and_type',
        'delete_expired',
    ],
)
def test_i_token_repository_has_methods(method_name):
    assert hasattr(
        ITokenRepository, method_name
    ), f"Falta el método '{method_name}' en ITokenRepository"


@pytest.mark.parametrize(
    'method_name',
    [
        'create',
        'get_by_token',
        'mark_as_used',
        'deleted',
        'delete_by_user_and_type',
        'find_active_by_user_and_type',
        'delete_expired',
    ],
)
def test_i_token_repository_methods_are_abstract(method_name):
    meth = getattr(ITokenRepository, method_name, None)
    assert getattr(
        meth, '__isabstractmethod__', False
    ), f"El método '{method_name}' debe ser abstracto"


# ---------- Signatures & parameter types ----------
def _params_without_self(func):
    params = list(signature(func).parameters.keys())
    return [p for p in params if p not in ('self', 'cls')]


def test_create_method_parameters_and_types():
    create = getattr(ITokenRepository, 'create', None)
    params = _params_without_self(create)
    for expected in ('user_id', 'token', 'token_type', 'expires_in'):
        assert (
            expected in params
        ), f"El método 'create' debe tener un parámetro '{expected}'. Parámetros: {params}"

    hints = _hints(create)
    assert (
        hints.get('user_id') is uuid.UUID
    ), f"El parámetro 'user_id' debe ser uuid.UUID, se encontró: {hints.get('user_id')!r}"
    assert (
        hints.get('token') is str
    ), f"El parámetro 'token' debe ser str, se encontró: {hints.get('token')!r}"
    assert (
        hints.get('token_type') is TokenType
    ), f"El parámetro 'token_type' debe ser TokenType, se encontró: {hints.get('token_type')!r}"
    assert (
        hints.get('expires_in') is datetime.timedelta
    ), f"El parámetro 'expires_in' debe ser datetime.timedelta, se encontró: {hints.get('expires_in')!r}"


def test_get_by_token_parameters_and_type():
    get = getattr(ITokenRepository, 'get_by_token', None)
    params = _params_without_self(get)
    assert (
        'token_value' in params
    ), f"El método 'get_by_token' debe tener 'token_value'. Parámetros: {params}"
    hints = _hints(get)
    assert (
        hints.get('token_value') is str
    ), f"El parámetro 'token_value' debe ser str, se encontró: {hints.get('token_value')!r}"


def test_mark_as_used_and_deleted_parameters_and_type():
    for name in ('mark_as_used', 'deleted'):
        meth = getattr(ITokenRepository, name, None)
        params = _params_without_self(meth)
        assert (
            'token' in params
        ), f"El método '{name}' debe tener 'token'. Parámetros: {params}"
        hints = _hints(meth)
        assert (
            hints.get('token') is str
        ), f"El parámetro 'token' en '{name}' debe ser str, se encontró: {hints.get('token')!r}"


def test_delete_by_user_and_type_parameters_and_types():
    meth = getattr(ITokenRepository, 'delete_by_user_and_type', None)
    params = _params_without_self(meth)
    assert (
        'token_type' in params and 'user_id' in params
    ), f'Parámetros esperados: token_type, user_id. Encontrados: {params}'
    hints = _hints(meth)
    assert (
        hints.get('token_type') is TokenType
    ), f"El parámetro 'token_type' debe ser TokenType, se encontró: {hints.get('token_type')!r}"
    assert (
        hints.get('user_id') is uuid.UUID
    ), f"El parámetro 'user_id' debe ser uuid.UUID, se encontró: {hints.get('user_id')!r}"


def test_find_active_by_user_and_type_parameters_and_types():
    meth = getattr(ITokenRepository, 'find_active_by_user_and_type', None)
    params = _params_without_self(meth)
    assert (
        'token_type' in params and 'user_id' in params
    ), f'Parámetros esperados: token_type, user_id. Encontrados: {params}'
    hints = _hints(meth)
    assert (
        hints.get('token_type') is TokenType
    ), f"El parámetro 'token_type' debe ser TokenType, se encontró: {hints.get('token_type')!r}"
    assert (
        hints.get('user_id') is uuid.UUID
    ), f"El parámetro 'user_id' debe ser uuid.UUID, se encontró: {hints.get('user_id')!r}"


# ---------- Return annotations ----------
def test_create_returns_token():
    ret = _hints(getattr(ITokenRepository, 'create')).get('return')
    assert (
        ret is Token
    ), f"El método 'create' debe declarar retorno 'Token', se encontró: {ret!r}"


def test_get_by_token_returns_optional_token():
    for name in ('get_by_token', 'find_active_by_user_and_type'):
        ret = _hints(getattr(ITokenRepository, name)).get('return')
        assert (
            ret is Optional[Token]
        ), f"El método '{name}' debe declarar retorno 'Optional[Token]', se encontró: {ret!r}"


def test_mark_and_deleted_and_delete_by_user_and_type_return_none():
    for name in ('mark_as_used', 'deleted', 'delete_by_user_and_type'):
        ret = _hints(getattr(ITokenRepository, name)).get('return')
        assert ret is type(
            None
        ), f"El método '{name}' debe declarar retorno 'None', se encontró: {ret!r}"


def test_delete_expired_returns_int():
    ret = _hints(getattr(ITokenRepository, 'delete_expired')).get('return')
    assert (
        ret is int
    ), f"El método 'delete_expired' debe declarar retorno int, se encontró: {ret!r}"


# ---------- Behavior: raise NotImplementedError (unbound call) ----------
def test_get_raises_not_implemented():
    get = getattr(ITokenRepository, 'get_by_token', None)
    with pytest.raises(NotImplementedError):
        get(None, 'token')


def test_create_raises_not_implemented():
    create = getattr(ITokenRepository, 'create', None)
    with pytest.raises(NotImplementedError):
        create(
            None,
            uuid.uuid4(),
            'token',
            TokenType.VERIFICATION,
            datetime.timedelta(minutes=5),
        )


def test_mark_as_used_raises_not_implemented():
    mark = getattr(ITokenRepository, 'mark_as_used', None)
    with pytest.raises(NotImplementedError):
        mark(None, 'token')


def test_deleted_raises_not_implemented():
    deleted = getattr(ITokenRepository, 'deleted', None)
    with pytest.raises(NotImplementedError):
        deleted(None, 'token')


def test_delete_by_user_and_type_raises_not_implemented():
    delete = getattr(ITokenRepository, 'delete_by_user_and_type', None)
    with pytest.raises(NotImplementedError):
        delete(None, TokenType.VERIFICATION, uuid.uuid4())


def test_delete_expired_raises_not_implemented():
    delete = getattr(ITokenRepository, 'delete_expired', None)
    with pytest.raises(NotImplementedError):
        delete(None)
