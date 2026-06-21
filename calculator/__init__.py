"""Калькулятор математических выражений."""

from typing import Dict, Literal, Optional, Union

from .core import evaluate_expression
from .exceptions import CalculatorError, EvaluationError, ParseError, TokenizeError

__version__ = "1.0.0"

__all__ = [
    "calculator",
    "Calculator",
    "CalculatorError",
    "TokenizeError",
    "ParseError",
    "EvaluationError",
]


def calculator(
    expression: str,
    *,
    verbose: bool = False,
    variables: Optional[Dict[str, Union[float, int]]] = None,
    precision: Optional[int] = None,
    angle_mode: Literal["rad", "deg"] = "rad",
) -> Union[int, float]:
    """Вычисляет математическое выражение.

    Args:
        expression: строка с выражением
        verbose: логировать шаги вычисления
        variables: значения переменных
        precision: количество знаков после запятой
        angle_mode: режим углов ("rad" | "deg")

    Returns:
        int — если результат целочисленный, иначе float

    Raises:
        CalculatorError — ошибки вычисления
        ZeroDivisionError — деление на ноль
    """
    return evaluate_expression(
        expression=expression,
        verbose=verbose,
        variables=variables,
        precision=precision,
        angle_mode=angle_mode,
    )


class Calculator:
    def __init__(
        self,
        *,
        verbose: bool = False,
        variables: Optional[Dict[str, Union[float, int]]] = None,
        precision: Optional[int] = None,
        angle_mode: Literal["rad", "deg"] = "rad",
    ):
        self.verbose = verbose
        self.variables = variables or {}
        self.precision = precision
        self.angle_mode = angle_mode

    def evaluate(self, expression: str) -> Union[int, float]:
        return calculator(
            expression,
            verbose=self.verbose,
            variables=self.variables,
            precision=self.precision,
            angle_mode=self.angle_mode,
        )
