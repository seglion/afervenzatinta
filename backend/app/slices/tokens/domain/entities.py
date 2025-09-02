# filepath: /workspace/backend/app/tests/units/slices/tokens/domain/test_domain.py

import datetime
import uuid

from pydantic import BaseModel, Field

from .values_objects import TokenType  # type: ignore


class Token(BaseModel):
    id:  uuid.UUID = Field(default_factory=uuid.uuid4)# noqa: B018
    token : str
    user_id : uuid.UUID
    token_type : TokenType
    expired_at : datetime.datetime
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    is_used : bool = False

    def is_valid(self)-> bool:
            return not self.is_used and self.expired_at > datetime.datetime.now(datetime.timezone.utc)
