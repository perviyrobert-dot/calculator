"""Узлы AST для математических выражений."""

from typing import List, Optional


class ASTNode:
    """Базовый класс для узлов AST."""
    def __init__(self, position: Optional[int] = None) -> None:
        self.position = position


class NumberNode(ASTNode):
    """Узел для чисел."""
    def __init__(self, value: float, position: Optional[int] = None) -> None:
        super().__init__(position)
        self.value: float = value


class VariableNode(ASTNode):
    """Узел для переменных."""
    def __init__(self, name: str, position: Optional[int] = None) -> None:
        super().__init__(position)
        self.name: str = name


class BinaryOpNode(ASTNode):
    """Узел для бинарных операций."""
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, position: Optional[int] = None) -> None:
        super().__init__(position)
        self.left: ASTNode = left
        self.operator: str = operator
        self.right: ASTNode = right


class UnaryOpNode(ASTNode):
    """Узел для унарных операций."""
    def __init__(self, operator: str, operand: ASTNode, position: Optional[int] = None) -> None:
        super().__init__(position)
        self.operator: str = operator
        self.operand: ASTNode = operand


class PercentNode(ASTNode):
    """Узел для унарного процента."""
    def __init__(self, operand: ASTNode, position: Optional[int] = None) -> None:
        super().__init__(position)
        self.operand: ASTNode = operand


class FunctionCallNode(ASTNode):
    """Узел для вызова функции."""
    def __init__(self, name: str, arguments: List[ASTNode], position: Optional[int] = None) -> None:
        super().__init__(position)
        self.name: str = name
        self.arguments: List[ASTNode] = arguments


class AssignmentNode(ASTNode):
    """Узел для присваивания."""
    def __init__(self, variable: str, expression: ASTNode, position: Optional[int] = None) -> None:
        super().__init__(position)
        self.variable: str = variable
        self.expression: ASTNode = expression


class ProgramNode(ASTNode):
    """Узел для программы (последовательность выражений)."""
    def __init__(self, statements: List[ASTNode], position: Optional[int] = None) -> None:
        super().__init__(position)
        self.statements: List[ASTNode] = statements
