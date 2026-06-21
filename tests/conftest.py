"""Фикстуры для тестов."""

import pytest

from calculator import calculator


@pytest.fixture
def calc():
    return calculator
