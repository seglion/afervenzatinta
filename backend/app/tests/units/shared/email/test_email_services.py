from abc import ABC
from inspect import signature
from typing import get_type_hints

from pydantic import EmailStr

from app.shared.email.services import IEmailService  # type: ignore


def test_iemailservice_exists():
    assert 'IEmailService' in globals(), 'El servicio IEmailService no está definida.'


def test_iemailservice_is_ABC():
    assert issubclass(IEmailService, ABC), 'IEmailService no hereda de ABC'


def test_iemailservice_has_methods():
    # Aquí podrías listar los métodos esperados y verificar su existencia
    expected_methods = [
        'send_verification_email',
        'send_password_reset_email',
    ]  # Agrega los nombres de los métodos esperados
    for method in expected_methods:
        assert hasattr(
            IEmailService, method
        ), f"Falta el método '{method}' en IEmailService"


def test_iemailservice_all_methods_are_abstract():
    expected_methods = [
        'send_verification_email',
        'send_password_reset_email',
    ]  # Agrega los nombres de los métodos esperados
    for method in expected_methods:
        meth = getattr(IEmailService, method, None)
        assert getattr(
            meth, '__isabstractmethod__', False
        ), f"El método '{method}' debe ser abstracto"


def test_iemailservice_methods_signatures_and_types():
    expected_methods = {
        'send_verification_email': ['to_email', 'verification_token'],
        'send_password_reset_email': ['to_email', 'reset_token'],
    }  # Agrega los nombres de los métodos esperados y sus parámetros si es necesario

    for method, params in expected_methods.items():
        meth = getattr(IEmailService, method, None)
        assert meth is not None, f"El método '{method}' no existe en IEmailService"
        meth_params = list(signature(meth).parameters.keys())
        # Excluir 'self' de la comparación
        meth_params = [p for p in meth_params if p != 'self']
        assert (
            meth_params == params
        ), f"El método '{method}' tiene parámetros incorrectos. Esperado: {params}, Encontrado: {meth_params}"
        # Aquí podrías agregar verificaciones adicionales para los tipos de los parámetros si es necesario
        hints = get_type_hints(meth)
        for param in params:
            assert (
                param in hints
            ), f"El parámetro '{param}' en el método '{method}' no tiene una anotación de tipo."
            if param == 'to_email':
                assert (
                    hints[param] is EmailStr
                ), f"El parámetro 'to_email' en el método '{method}' debe ser de tipo EmailStr."
            else:
                assert (
                    hints[param] is str
                ), f"El parámetro '{param}' en el método '{method}' debe ser de tipo str."
        # Verificar que el tipo de retorno sea None
        ret = hints.get('return', None)
        assert ret is type(
            None
        ), f"El método '{method}' debe declarar retorno None, se encontró: {ret!r}"
