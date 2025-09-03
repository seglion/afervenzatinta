from abc import ABC, abstractmethod

from pydantic import EmailStr


class IEmailService(ABC):
    @abstractmethod
    async def send_verification_email(
        self, to_email: EmailStr, verification_token: str
    ) -> None:
        """Envía un email para la verificación de la cuenta."""
        raise NotImplementedError(
            'Debe implementar el metodo abstracto send_verification_email'
        )

    @abstractmethod
    async def send_password_reset_email(
        self, to_email: EmailStr, reset_token: str
    ) -> None:
        """Envía un email para el reseteo de la contraseña."""
        raise NotImplementedError(
            'Debe implementar el metodo abstracto send_password_reset_email'
        )

