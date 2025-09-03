import logging
from inspect import signature
from typing import get_type_hints

from pydantic import EmailStr

from app.infrastructure.services.email.log_email_service import (  # type: ignore
    LogEmailService,  # type: ignore
)
from app.shared.email.services import IEmailService  # type: ignore


def test_log_email_service_exists():
    assert (
        'LogEmailService' in globals()
    ), 'El servicio LogEmailService no está definida'


def test_log_email_service_inherits_from_iemailservice():
    assert issubclass(
        LogEmailService, IEmailService
    ), 'LogEmailService no hereda de IEmailService'


def test_log_email_service_send_verification_email():
    service = LogEmailService()
    assert hasattr(
        service, 'send_verification_email'
    ), "LogEmailService no tiene el método 'send_verification_email'"
    method = service.send_verification_email
    assert callable(method), "'send_verification_email' no es un método callable"


def test_log_email_service_send_password_reset_email():
    service = LogEmailService()
    assert hasattr(
        service, 'send_password_reset_email'
    ), "LogEmailService no tiene el método 'send_password_reset_email'"
    method = service.send_password_reset_email
    assert callable(method), "'send_password_reset_email' no es un método callable"


def test_log_email_service_methods_are_not_abstract():
    service = LogEmailService()
    send_verification_email = getattr(service, 'send_verification_email', None)
    assert not getattr(
        send_verification_email, '__isabstractmethod__', False
    ), "'send_verification_email' debe ser una implementación concreta"

    send_password_reset_email = getattr(service, 'send_password_reset_email', None)
    assert not getattr(
        send_password_reset_email, '__isabstractmethod__', False
    ), "'send_password_reset_email' debe ser una implementación concreta"  # noqa: E501


def test_log_email_service_methods_signatures_and_types():
    service = LogEmailService()
    expected_methods = {
        'send_verification_email': ['to_email', 'verification_token'],
        'send_password_reset_email': ['to_email', 'reset_token'],
    }

    for method_name, params in expected_methods.items():
        meth = getattr(service, method_name, None)
        assert (
            meth is not None
        ), f"El método '{method_name}' no existe en LogEmailService"
        meth_params = list(signature(meth).parameters.keys())
        # Excluir 'self' de la comparación
        meth_params = [p for p in meth_params if p != 'self']
        assert (
            meth_params == params
        ), f"El método '{method_name}' tiene parámetros incorrectos. Esperado: {params}, Encontrado: {meth_params}"
        hints = get_type_hints(meth)
        for param in params:
            assert (
                param in hints
            ), f"El parámetro '{param}' en el método '{method_name}' no tiene una anotación de tipo."
            if param == 'to_email':
                assert (
                    hints[param] is EmailStr
                ), f"El parámetro 'to_email' en el método '{method_name}' debe ser de tipo EmailStr, se encontró: {hints[param]!r}"
            else:
                assert (
                    hints[param] is str
                ), f"El parámetro '{param}' en el método '{method_name}' debe ser de tipo str, se encontró: {hints[param]!r}"
        ret = hints.get('return')
        assert ret is type(
            None
        ), f"El método '{method_name}' debe declarar retorno None, se encontró: {ret!r}"  # noqa: E501


def test_log_email_service_methods_execution(caplog):
    service = LogEmailService()
    test_email = 'example@example.com'
    test_token = 'testtoken123'
    with caplog.at_level(logging.INFO):
        import asyncio

        asyncio.run(service.send_verification_email(test_email, test_token))
        asyncio.run(service.send_password_reset_email(test_email, test_token))

    verification_logs = [
        '--- SIMULANDO ENVÍO DE EMAIL ---',
        f'Destinatario: {test_email}',
        'Asunto: Verifica tu cuenta',
        f'Token: {test_token}',
        '-----------------------------',
    ]
    reset_logs = [
        '--- SIMULANDO ENVÍO DE EMAIL ---',
        f'Destinatario: {test_email}',
        'Asunto: Resetea tu contraseña',
        f'Token: {test_token}',
        '-----------------------------',
    ]
    for log in verification_logs:
        assert (
            log in caplog.text
        ), f"Falta el log esperado en 'send_verification_email': {log}"
    for log in reset_logs:
        assert (
            log in caplog.text
        ), f"Falta el log esperado en 'send_password_reset_email': {log}"
