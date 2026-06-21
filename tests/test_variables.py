"""Тесты переменных."""

import pytest

from calculator import calculator


@pytest.mark.parametrize(
    "expression,variables,expected",
    [
        ("x + y", {"x": 10, "y": 5}, 15),
        ("x * 2", {"x": 3.5}, 7.0),
        ("x**2 + y**2", {"x": 3, "y": 4}, 25),
        ("x = 2; x * 3", {}, 6),
        ("a = 1; b = a + 2; a + b", {}, 4),
    ],
)
def test_variables(expression, variables, expected):
    result = calculator(expression, variables=variables)
    if isinstance(expected, float):
        assert result == pytest.approx(expected, rel=1e-9)
    else:
        assert result == expected
