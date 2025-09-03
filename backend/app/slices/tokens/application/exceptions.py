class TokenException(Exception):
    """Excepción base para errores relacionados con tokens."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidTokenException(TokenException):
    """
    Se lanza cuando un token es inválido porque no se encuentra,
    es de un tipo incorrecto o ha sido malformado.
    """

    def __init__(
        self,
        message: str = 'El token proporcionado es inválido o no ha sido encontrado.',
    ):
        super().__init__(message)


class ExpiredTokenException(TokenException):
    """
    Se lanza cuando un token es válido en su forma, pero su fecha
    de expiración ya ha pasado.
    """

    def __init__(self, message: str = 'El token ha expirado y ya no es válido.'):
        super().__init__(message)
