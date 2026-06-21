"""Реестр математических функций."""

import math
from typing import Callable, Dict, Tuple

FunctionInfo = Tuple[int, Callable[..., float]]


def _factorial(n: float) -> float:
    """Вычисление факториала с проверками."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("factorial requires non-negative integer")
    return float(math.factorial(int(n)))


FUNCTIONS: Dict[str, FunctionInfo] = {
    "sqrt": (1, math.sqrt),
    "abs": (1, abs),
    "pow": (2, math.pow),
    "min": (-1, min),
    "max": (-1, max),
    "floor": (1, math.floor),
    "ceil": (1, math.ceil),
    "round": (1, round),
    "log": (1, math.log),
    "ln": (1, math.log),
    "log10": (1, math.log10),
    "exp": (1, math.exp),
    "sin": (1, math.sin),
    "cos": (1, math.cos),
    "tan": (1, math.tan),
    "factorial": (1, _factorial),
}
