import datetime
import sys
from types import NoneType
import uuid
from abc import ABC, abstractmethod
from inspect import signature
from typing import Optional, get_type_hints

import pytest

from app.slices.tokens.domain.entities import Token
from app.slices.tokens.domain.values_objects import TokenType


class ITokenRepository(ABC):
    @abstractmethod# noqa: B024
    def create(self,user_id: uuid.UUID, token: str, token_type: TokenType,expires_in: datetime.timedelta)-> Token:  # noqa: B027
        raise NotImplementedError("Debe implementar el metodo abstracto create") 

    @abstractmethod
    def get_by_token(self,token_value:str)-> Optional[Token]:
        raise NotImplementedError("Debe implementar el metodo abstracto get") 
    
    @abstractmethod
    def mark_as_used(self,token: str)->None:
        raise NotImplementedError("Debe implementar el metodo abstracto mark_as_used") 







def test_i_token_repository_interface_exists():
    assert 'ITokenRepository' in globals(), "La clase TokenType no se encontró."

def test_i_token_repository_inherits_from_abc():
    assert issubclass(ITokenRepository, ABC), "ITokenRepository no hereda de ABC"  # noqa: W292

#
# existencia de metodos

def test_i_token_repository_has_create_method():
    assert hasattr(ITokenRepository, 'create'), "Falta el método 'create' en ITokenRepository"

def test_i_token_repository_has_get_by_token_method():
    assert hasattr(ITokenRepository, 'get_by_token'), "Falta el método 'get_by_token' en ITokenRepository"

def test_i_token_repository_has_mark_as_used_method():
    assert hasattr(ITokenRepository, 'mark_as_used'), "Falta el método 'mark_as_used' en ITokenRepository"

#Comprobacion de que son metodos abstractos
def test_i_token_repository_create_method_is_abstract_method():
    create = getattr(ITokenRepository, "create", None)
    assert getattr(create, "__isabstractmethod__", False), "El método 'create' debe ser abstracto"
def test_i_token_repository_get_by_token_method_is_abstract_method():
    get = getattr(ITokenRepository, "get_by_token", None)
    assert getattr(get, "__isabstractmethod__", False), "El método 'get' debe ser abstracto"
def test_i_token_repository_mark_as_used_method_is_abstract_method():
    mark = getattr(ITokenRepository, "mark_as_used", None)
    assert getattr(mark, "__isabstractmethod__", False), "El método 'mark_as_used' debe ser abstracto"



#comprobacion de firmas y tipos de datos
def test_i_token_repository_create_method_parameters():
    create = getattr(ITokenRepository, "create", None)

    sig = signature(create)
    params = list(sig.parameters.keys())
    # Ignorar 'self' o 'cls' si están presentes
    params_without_self = [p for p in params if p not in ("self", "cls")]

    assert "user_id" in params_without_self, f"El método 'create' debe tener un parámetro 'user_id'. Parámetros: {params}"
    assert "token" in params_without_self, f"El método 'create' debe tener un parámetro 'user_id'. Parámetros: {params}"
    assert "token_type" in params_without_self, f"El método 'create' debe tener un parámetro 'token_type'. Parámetros: {params}"
    assert "expires_in" in params_without_self, f"El método 'create' debe tener un parámetro 'expires_in'. Parámetros: {params}"

    hints = get_type_hints(create, vars(sys.modules[ITokenRepository.__module__]))
    user_hint = hints.get("user_id", None)
    token_hint = hints.get("token", None)
    token_type_hint = hints.get("token_type", None)
    expires_in_hint = hints.get("expires_in", None)

    assert user_hint is uuid.UUID, f"El parámetro 'user_id' debe estar anotado como uuid.UUID, se encontró: {user_hint!r}"
    assert token_hint is str, f"El parámetro 'token' debe estar anotado como str, se encontró: {token_hint!r}"
    assert token_type_hint is TokenType, f"El parámetro 'token_type' debe estar anotado como Token_Type, se encontró: {token_type_hint!r}"
    assert expires_in_hint is datetime.timedelta, f"El parámetro 'expires_in' debe estar anotado como datetime.delta, se encontró: {expires_in_hint!r}"

def test_i_token_repository_get_by_token_method_parameters():
    get = getattr(ITokenRepository, "get_by_token", None)

    sig = signature(get)
    params = list(sig.parameters.keys())
    # Ignorar 'self' o 'cls' si están presentes
    params_without_self = [p for p in params if p not in ("self", "cls")]

    assert "token_value" in params_without_self, f"El método 'get_by_token' debe tener un parámetro 'token_value'. Parámetros: {params}"

    hints = get_type_hints(get, vars(sys.modules[ITokenRepository.__module__]))
    token_value_hint = hints.get("token_value", None)
    assert token_value_hint is str, f"El parámetro 'token_value' debe estar anotado como str, se encontró: {token_value_hint!r}"

def test_i_token_repository_mark_as_used_method_parameters():
    mark = getattr(ITokenRepository, "mark_as_used", None)

    sig = signature(mark)
    params = list(sig.parameters.keys())
    # Ignorar 'self' o 'cls' si están presentes
    params_without_self = [p for p in params if p not in ("self", "cls")]

    assert "token" in params_without_self, f"El método 'mark_as_used' debe tener un parámetro 'token'. Parámetros: {params}"

    hints = get_type_hints(mark, vars(sys.modules[ITokenRepository.__module__]))
    token_hint = hints.get("token", None)
    assert token_hint is str, f"El parámetro 'token' debe estar anotado como str, se encontró: {token_hint!r}"




#TEST PARA COMPROBAR ANOTACION DE VALORES DE RETORNO

def test_itokenrepository_create_returns_token():
    add = getattr(ITokenRepository, "create", None)


    # Resuelve anotaciones usando el espacio de nombres del módulo donde está la interfaz
    hints = get_type_hints(add, vars(sys.modules[ITokenRepository.__module__]))
    ret = hints.get("return", None)

    assert ret is Token, f"El método 'create' debe declarar retorno 'Token', se encontró: {ret!r}"

def test_itokenrepository_get_returns_token():
    get = getattr(ITokenRepository, "get_by_token", None)


    # Resuelve anotaciones usando el espacio de nombres del módulo donde está la interfaz
    hints = get_type_hints(get, vars(sys.modules[ITokenRepository.__module__]))
    ret = hints.get("return", None)

    assert ret is Optional[Token], f"El método 'get_by_token' debe declarar retorno 'Token', se encontró: {ret!r}"

def test_itokenrepository_mark_as_used_returns_None():
    mark = getattr(ITokenRepository, "mark_as_used", None)


    # Resuelve anotaciones usando el espacio de nombres del módulo donde está la interfaz
    hints = get_type_hints(mark, vars(sys.modules[ITokenRepository.__module__]))
    ret = hints.get("return", None)

    assert ret is type(None), f"El método 'mark_as_used' debe declarar retorno 'None', se encontró: {ret!r}"


#Test para raise error

def test_i_token_repository_get_method_raise_not_implemented():
    get = getattr(ITokenRepository, "get_by_token", None)
    with pytest.raises(NotImplementedError):
        get(None,  "token")

def test_i_token_repository_create_method_raise_not_implemented():
    create = getattr(ITokenRepository, "create", None)
    with pytest.raises(NotImplementedError):
        create(None, uuid.uuid4(), "token", TokenType.VERIFICATION, datetime.timedelta(minutes=5))
def test_itokenrepository_mark_as_used_method_raise_not_implemented():
    mark = getattr(ITokenRepository, "mark_as_used", None)
    with pytest.raises(NotImplementedError):
        mark(None,  "token")