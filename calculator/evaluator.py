"""Вычислитель AST."""

import logging
import math
from typing import Dict, Optional, Union

from .ast_nodes import (
    ASTNode,
    AssignmentNode,
    BinaryOpNode,
    FunctionCallNode,
    NumberNode,
    PercentNode,
    ProgramNode,
    UnaryOpNode,
    VariableNode,
)
from .constants import CONSTANTS
from .exceptions import EvaluationError
from .functions import FUNCTIONS


class Evaluator:
    """Вычислитель AST."""

    def __init__(self, verbose: bool = False, angle_mode: str = "rad") -> None:
        self.verbose = verbose
        self.angle_mode = angle_mode
        self.logger = logging.getLogger("calculator.evaluator")
        self.step = 0
        self.local_context: Dict[str, float] = {}

    def evaluate(
        self,
        node: ASTNode,
        variables: Optional[Dict[str, Union[float, int]]] = None,
        precision: Optional[int] = None,
    ) -> Union[float, int]:
        """Вычисление AST."""
        self.local_context = {**CONSTANTS}
        if variables:
            self.local_context.update({k: float(v) for k, v in variables.items()})
        self.step = 0

        result = self._evaluate_node(node)

        if precision is not None:
            result = round(result, precision)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        if isinstance(result, float) and result == 0.0:
            result = 0.0

        return result

    def _evaluate_node(self, node: ASTNode) -> float:
        """Вычисление узла AST."""
        if isinstance(node, NumberNode):
            return float(node.value)

        if isinstance(node, VariableNode):
            if node.name in self.local_context:
                return float(self.local_context[node.name])
            raise EvaluationError(f"unknown variable '{node.name}'")

        if isinstance(node, UnaryOpNode):
            operand = self._evaluate_node(node.operand)
            if node.operator == '-':
                return -operand
            return operand

        if isinstance(node, PercentNode):
            operand = self._evaluate_node(node.operand)
            return operand / 100.0

        if isinstance(node, BinaryOpNode):
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)

            if node.operator == '+':
                result = left + right
            elif node.operator == '-':
                result = left - right
            elif node.operator == '*':
                result = left * right
            elif node.operator == '/':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result = left / right
            elif node.operator == '//':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result = left // right
            elif node.operator == '%':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result = left % right
            elif node.operator == '**':
                if left == 0 and right == 0:
                    result = 1.0
                else:
                    result = left ** right
            else:
                raise EvaluationError(f"unknown operator '{node.operator}'")

            if self.verbose:
                self.step += 1
                self.logger.debug(
                    "step=%d op=%s operands=[%s, %s] result=%s",
                    self.step, node.operator, left, right, result
                )

            return result

        if isinstance(node, FunctionCallNode):
            return self._evaluate_function(node)

        if isinstance(node, AssignmentNode):
            value = self._evaluate_node(node.expression)
            self.local_context[node.variable] = value
            return value

        if isinstance(node, ProgramNode):
            result = 0.0
            for stmt in node.statements:
                result = self._evaluate_node(stmt)
            return result

        raise EvaluationError(f"unknown AST node: {type(node)}")

    def _evaluate_function(self, node: FunctionCallNode) -> float:
        """Вычисление вызова функции."""
        if node.name not in FUNCTIONS:
            raise EvaluationError(f"unknown function '{node.name}'")

        arity, func = FUNCTIONS[node.name]

        if arity != -1 and len(node.arguments) != arity:
            raise EvaluationError(
                f"{node.name}() takes {arity} argument(s), got {len(node.arguments)}"
            )

        if arity == -1 and len(node.arguments) == 0:
            raise EvaluationError(f"{node.name}() requires at least one argument")

        args = [self._evaluate_node(arg) for arg in node.arguments]

        if node.name in ('sin', 'cos', 'tan') and self.angle_mode == "deg":
            args[0] = math.radians(args[0])

        if node.name == 'sqrt' and args[0] < 0:
            raise EvaluationError("cannot take sqrt of negative number")

        if node.name in ('log', 'ln') and args[0] <= 0:
            raise EvaluationError("logarithm argument must be positive")

        if node.name == 'factorial':
            if not isinstance(args[0], (int, float)) or not args[0].is_integer() or args[0] < 0:
                raise EvaluationError("factorial requires non-negative integer")
            args[0] = int(args[0])

        try:
            result = func(*args)
        except Exception as e:
            raise EvaluationError(f"error in {node.name}: {str(e)}")

        if self.verbose:
            self.step += 1
            self.logger.debug(
                "step=%d op=%s operands=%s result=%s",
                self.step, node.name, args, result
            )

        return float(result)
