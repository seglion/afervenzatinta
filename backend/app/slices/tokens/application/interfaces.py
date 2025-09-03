import datetime
import uuid
from abc import ABC, abstractmethod
from typing import Optional

from app.slices.tokens.domain.entities import Token
from app.slices.tokens.domain.values_objects import TokenType


class ITokenRepository(ABC):
    @abstractmethod  # noqa: B024
    def create(
        self,
        user_id: uuid.UUID,
        token: str,
        token_type: TokenType,
        expires_in: datetime.timedelta,
    ) -> Token:  # noqa: B027
        raise NotImplementedError('Debe implementar el metodo abstracto create')

    @abstractmethod
    async def  get_by_token(self, token_value: str) -> Optional[Token]:
        raise NotImplementedError('Debe implementar el metodo abstracto get')

    @abstractmethod
    async def mark_as_used(self, token: str) -> None:
        raise NotImplementedError('Debe implementar el metodo abstracto mark_as_used')

    @abstractmethod
    async def deleted(self, token: str) -> None:
        raise NotImplementedError('Debe implementar el metodo abstracto deleted')

    @abstractmethod
    async def delete_by_user_and_type(
        self, token_type: TokenType, user_id: uuid.UUID
    ) -> None:
        raise NotImplementedError(
            'Debe implementar el metodo abstracto delete_by_user_and_type'
        )

    @abstractmethod
    async def find_active_by_user_and_type(
        self, token_type: TokenType, user_id: uuid.UUID
    ) -> Optional[Token]:
        raise NotImplementedError(
            'Debe implementar el metodo abstracto find_active_by_user_and_type'
        )

    @abstractmethod
    async def delete_expired(self) -> int:
        raise NotImplementedError('Debe implementar el metodo abstracto delete_expired')
