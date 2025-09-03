
import logging

from pydantic import EmailStr

from app.shared.email.services import (  # type: ignore
    IEmailService,  # pyright: ignore[reportMissingImports]
)


class LogEmailService(IEmailService):
    async def send_verification_email(
        self, to_email: EmailStr, verification_token: str
    ) -> None:
        logging.info("--- SIMULANDO ENVÍO DE EMAIL ---")
        logging.info(f"Destinatario: {to_email}")
        logging.info("Asunto: Verifica tu cuenta")
        logging.info(f"Token: {verification_token}")
        logging.info("-----------------------------")

    async def send_password_reset_email(
        self, to_email: EmailStr, reset_token: str
    ) -> None:
        logging.info("--- SIMULANDO ENVÍO DE EMAIL ---")
        logging.info(f"Destinatario: {to_email}")
        logging.info("Asunto: Resetea tu contraseña")
        logging.info(f"Token: {reset_token}")
        logging.info("-----------------------------")
