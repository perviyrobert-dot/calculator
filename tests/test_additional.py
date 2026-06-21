"""Дополнительные тесты для покрытия."""

import logging


from calculator import calculator


def test_verbose_mode_with_logging(caplog):
    """Тестирование verbose режима с логированием."""
    caplog.set_level(logging.DEBUG)

    result = calculator("2+3*4", verbose=True)
    assert result == 14

    # Проверяем, что логи были записаны
    assert len(caplog.records) >= 2

    # Проверяем структуру логов
    log_messages = [record.getMessage() for record in caplog.records]
    assert any("step=1 op=*" in msg for msg in log_messages)
    assert any("step=2 op=+" in msg for msg in log_messages)


def test_verbose_off(caplog):
    """Тестирование что verbose=False не логирует."""
    caplog.set_level(logging.DEBUG)

    calculator("2+3", verbose=False)
    assert len(caplog.records) == 0


def test_advanced_operations():
    """Тестирование продвинутых операций."""
    # Проверка работы с разными типами чисел
    assert calculator("1.5e3") == 1500.0
    assert calculator("1_000") == 1000

    # Проверка составных выражений
    assert calculator("(2+3)*(4+5)") == 45

    # Проверка отрицательных чисел
    assert calculator("-5 + -3") == -8

    # Проверка вложенных функций
    assert calculator("sqrt(abs(-16))") == 4.0


def test_power_edge_cases():
    """Тестирование граничных случаев степени."""
    assert calculator("2**-1") == 0.5
    assert calculator("(-2)**2") == 4
    assert calculator("0**0") == 1


def test_percent_edge_cases():
    """Тестирование граничных случаев процента."""
    assert calculator("100% + 100%") == 2.0
    assert calculator("(1+2)%") == 0.03


def test_assignment_chain():
    """Тестирование цепочки присваиваний."""
    result = calculator("x = 5; y = x + 2; y * 2")
    assert result == 14


def test_assignment_overwrite():
    """Тестирование перезаписи переменной."""
    result = calculator("x = 5; x = 10; x + 2")
    assert result == 12


def test_unary_operators():
    """Тестирование унарных операторов."""
    assert calculator("+-5") == -5
    assert calculator("-+5") == -5
    assert calculator("---5") == -5


def test_factorial_edge_cases():
    """Тестирование граничных случаев факториала."""
    assert calculator("factorial(0)") == 1
    assert calculator("factorial(1)") == 1
    assert calculator("factorial(2)") == 2
