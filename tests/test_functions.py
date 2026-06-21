"""Тесты функций."""

import pytest

from calculator import calculator


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("sqrt(16)", 4),
        ("abs(-5)", 5),
        ("pow(2, 10)", 1024),
        ("min(3, 1, 2)", 1),
        ("max(3, 1, 2)", 3),
        ("floor(3.7)", 3),
        ("ceil(3.2)", 4),
        ("round(3.5)", 4),
        ("log(e)", 1.0),
        ("ln(e)", 1.0),
        ("log10(1000)", 3.0),
        ("exp(0)", 1.0),
        ("factorial(0)", 1),
        ("factorial(5)", 120),
        ("factorial(10)", 3628800),
    ],
)
def test_functions(expression, expected):
    result = calculator(expression)
    if isinstance(expected, float):
        assert result == pytest.approx(expected, rel=1e-9)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "expression,angle_mode,expected",
    [
        ("sin(0)", "rad", 0.0),
        ("sin(pi/2)", "rad", 1.0),
        ("sin(90)", "deg", 1.0),
        ("cos(0)", "rad", 1.0),
        ("cos(60)", "deg", 0.5),
        ("tan(45)", "deg", 1.0),
    ],
)
def test_trigonometry(expression, angle_mode, expected):
    result = calculator(expression, angle_mode=angle_mode)
    assert result == pytest.approx(expected, rel=1e-9)
