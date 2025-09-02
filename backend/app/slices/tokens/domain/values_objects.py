from enum import Enum


class TokenType(str, Enum):
    """Clase para representar los tipos de tokens."""
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"