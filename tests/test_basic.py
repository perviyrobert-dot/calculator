"""Тесты базовых операций."""

import pytest

from calculator import calculator


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("2+3", 5),
        ("10-4", 6),
        ("6*7", 42),
        ("15/3", 5),
        ("15/4", 3.75),
        ("17%5", 2),
        ("17//5", 3),
        ("50%", 0.5),
        ("200*10%", 20.0),
        ("(100+50)%", 1.5),
        ("2+3*4", 14),
        ("(2+3)*4", 20),
        ("10-2*3", 4),
        ("100/10/2", 5.0),
    ],
)
def test_basic_operations(expression, expected):
    result = calculator(expression)
    if isinstance(expected, float):
        assert result == pytest.approx(expected, rel=1e-9)
    else:
        assert result == expected
