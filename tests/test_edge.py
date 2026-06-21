"""Тесты граничных случаев."""

import pytest

from calculator import EvaluationError, ParseError, TokenizeError, calculator


def test_empty_expression():
    with pytest.raises(ValueError, match="empty expression"):
        calculator("")
    with pytest.raises(ValueError, match="empty expression"):
        calculator("   ")


def test_invalid_character():
    with pytest.raises(TokenizeError):
        calculator("2 @ 3")


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculator("10/0")
    with pytest.raises(ZeroDivisionError):
        calculator("10//0")


def test_unbalanced_parentheses():
    # Незакрытая скобка
    with pytest.raises(ParseError):
        calculator("(2+3")
    # Лишняя закрывающая скобка
    with pytest.raises(ParseError):
        calculator("(2+3))")
    # Незакрытая скобка с функцией
    with pytest.raises(ParseError):
        calculator("sqrt(16")
    # Лишняя закрывающая скобка с функцией
    with pytest.raises(ParseError):
        calculator("sqrt(16))")


def test_unknown_variable():
    with pytest.raises(EvaluationError, match="unknown variable 'z'"):
        calculator("z + 1")


def test_unknown_function():
    with pytest.raises(EvaluationError):
        calculator("foo(1)")


def test_sqrt_negative():
    with pytest.raises(EvaluationError):
        calculator("sqrt(-1)")


def test_whitespace_handling():
    result = calculator("   2 + 3   ")
    assert result == 5
