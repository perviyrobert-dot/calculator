"""Иерархия исключений калькулятора."""

from typing import Optional


class CalculatorError(Exception):
    """Базовое исключение калькулятора."""
    pass


class TokenizeError(CalculatorError):
    """Ошибка токенизации."""
    def __init__(self, message: str, position: int):
        self.position = position
        super().__init__(f"{message} at position {position}")


class ParseError(CalculatorError):
    """Синтаксическая ошибка."""
    def __init__(self, message: str, position: Optional[int] = None):
        self.position = position
        if position is not None:
            super().__init__(f"{message} at position {position}")
        else:
            super().__init__(message)


class EvaluationError(CalculatorError):
    """Ошибка вычисления."""
    pass
