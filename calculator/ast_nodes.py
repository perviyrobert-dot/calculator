"""Узлы AST для математических выражений."""


class ASTNode:
    """Базовый класс для узлов AST."""

    def __init__(self, position=None):
        self.position = position


class NumberNode(ASTNode):
    """Узел для чисел."""

    def __init__(self, value, position=None):
        super().__init__(position)
        self.value = value


class VariableNode(ASTNode):
    """Узел для переменных."""

    def __init__(self, name, position=None):
        super().__init__(position)
        self.name = name


class BinaryOpNode(ASTNode):
    """Узел для бинарных операций."""

    def __init__(self, left, operator, right, position=None):
        super().__init__(position)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOpNode(ASTNode):
    """Узел для унарных операций."""

    def __init__(self, operator, operand, position=None):
        super().__init__(position)
        self.operator = operator
        self.operand = operand


class PercentNode(ASTNode):
    """Узел для унарного процента."""

    def __init__(self, operand, position=None):
        super().__init__(position)
        self.operand = operand


class FunctionCallNode(ASTNode):
    """Узел для вызова функции."""

    def __init__(self, name, arguments, position=None):
        super().__init__(position)
        self.name = name
        self.arguments = arguments


class AssignmentNode(ASTNode):
    """Узел для присваивания."""

    def __init__(self, variable, expression, position=None):
        super().__init__(position)
        self.variable = variable
        self.expression = expression


class ProgramNode(ASTNode):
    """Узел для программы (последовательность выражений)."""

    def __init__(self, statements, position=None):
        super().__init__(position)
        self.statements = statements
