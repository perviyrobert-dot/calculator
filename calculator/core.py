"""Оркестрация pipeline."""

from typing import Dict, Literal, Optional, Union

from .evaluator import Evaluator
from .parser import Parser


def evaluate_expression(
    expression: str,
    verbose: bool = False,
    variables: Optional[Dict[str, Union[float, int]]] = None,
    precision: Optional[int] = None,
    angle_mode: Literal["rad", "deg"] = "rad",
) -> Union[float, int]:
    if not expression or not expression.strip():
        raise ValueError("empty expression")

    expression = expression.strip()

    parser = Parser(expression)
    ast = parser.parse()

    evaluator = Evaluator(verbose=verbose, angle_mode=angle_mode)
    result = evaluator.evaluate(ast, variables=variables, precision=precision)

    if isinstance(result, float) and result == 0.0:
        result = 0.0

    return result
