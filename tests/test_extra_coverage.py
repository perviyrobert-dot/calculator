"""Дополнительные тесты для повышения покрытия кода."""

import pytest

from calculator import calculator, Calculator
from calculator.exceptions import (
    CalculatorError,
    EvaluationError,
    ParseError,
    TokenizeError,
)


def test_calculator_class():
    """Тестирование класса Calculator."""
    calc = Calculator()
    assert calc.evaluate("2+3") == 5

    calc = Calculator(verbose=True)
    assert calc.evaluate("2+3") == 5

    calc = Calculator(precision=2)
    assert calc.evaluate("10/3") == 3.33

    calc = Calculator(angle_mode="deg")
    assert calc.evaluate("sin(90)") == pytest.approx(1.0)


def test_error_messages():
    """Тестирование сообщений об ошибках."""
    # Проверка TokenizeError с позицией
    with pytest.raises(TokenizeError) as exc_info:
        calculator("2 @ 3")
    assert exc_info.value.position == 2

    # Проверка ParseError с позицией
    with pytest.raises(ParseError) as exc_info:
        calculator("2 +")
    assert exc_info.value.position is not None


def test_parse_error_without_position():
    """Тестирование ParseError без позиции."""
    error = ParseError("test error")
    assert error.position is None
    assert str(error) == "test error"


def test_evaluation_error():
    """Тестирование EvaluationError."""
    error = EvaluationError("test error")
    assert str(error) == "test error"


def test_calculator_error():
    """Тестирование базового исключения."""
    error = CalculatorError("test error")
    assert str(error) == "test error"


def test_negative_zero_normalization():
    """Тестирование нормализации -0.0."""
    result = calculator("-0.0")
    assert result == 0
    # Проверяем, что это целое число (int), а не float
    assert isinstance(result, int)


def test_large_factorial():
    """Тестирование большого факториала."""
    result = calculator("factorial(20)")
    assert result == 2432902008176640000


def test_precision_with_int_result():
    """Тестирование precision с целым результатом."""
    result = calculator("2+2", precision=2)
    assert result == 4
    assert isinstance(result, int)


def test_angle_mode_default():
    """Тестирование angle_mode по умолчанию."""
    result = calculator("sin(0)")
    assert result == 0.0


def test_variables_with_float_values():
    """Тестирование переменных с float значениями."""
    result = calculator("x + y", variables={"x": 1.5, "y": 2.5})
    assert result == 4.0


def test_complex_expression():
    """Тестирование сложного выражения."""
    result = calculator("sin(pi/2) + cos(0) * 2")
    assert result == pytest.approx(3.0, rel=1e-9)
