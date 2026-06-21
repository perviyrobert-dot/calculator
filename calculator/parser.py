"""Парсер с рекурсивным спуском."""

from typing import List, Optional

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
from .exceptions import ParseError
from .tokenizer import Lexer, Token, TokenType


class Parser:
    """Парсер с рекурсивным спуском."""

    def __init__(self, expression: str) -> None:
        self.lexer = Lexer(expression)
        self.tokens: List[Token] = self.lexer.tokenize()
        self.pos: int = 0
        self.current_token: Optional[Token] = self.tokens[0] if self.tokens else None
        self._paren_count: int = 0

    def parse(self) -> ProgramNode:
        """Разбор программы."""
        statements: List[ASTNode] = []

        while self.current_token and self.current_token.type != TokenType.EOF:
            if (
                self.current_token.type == TokenType.IDENTIFIER
                and self._peek_next() == TokenType.ASSIGN
            ):
                statements.append(self._parse_assignment())
            else:
                statements.append(self._parse_expression())

            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self._consume(TokenType.SEMICOLON)
            else:
                break

        if self._paren_count != 0:
            raise ParseError("unbalanced parentheses", 0)

        if self.current_token and self.current_token.type == TokenType.RPAREN:
            raise ParseError("unbalanced parentheses", self.current_token.position)

        return ProgramNode(statements)

    def _parse_expression(self) -> ASTNode:
        """Разбор выражения (сложение/вычитание)."""
        node = self._parse_term()

        while self.current_token and self.current_token.type == TokenType.OPERATOR:
            if self.current_token.value in ('+', '-'):
                op: str = self.current_token.value
                pos: int = self.current_token.position
                self._advance()
                right: ASTNode = self._parse_term()
                node = BinaryOpNode(left=node, operator=op, right=right, position=pos)
            else:
                break

        return node

    def _parse_term(self) -> ASTNode:
        """Разбор терма (умножение/деление/остаток)."""
        node = self._parse_factor()

        while self.current_token and self.current_token.type == TokenType.OPERATOR:
            if self.current_token.value in ('*', '/', '//', '%'):
                op = self.current_token.value
                pos = self.current_token.position
                self._advance()
                right = self._parse_factor()
                node = BinaryOpNode(left=node, operator=op, right=right, position=pos)
            else:
                break

        return node

    def _parse_factor(self) -> ASTNode:
        """Разбор фактора (степень)."""
        node = self._parse_unary()

        while self.current_token and self.current_token.type == TokenType.OPERATOR:
            if self.current_token.value == '**':
                pos = self.current_token.position
                self._advance()
                right = self._parse_factor()
                node = BinaryOpNode(left=node, operator='**', right=right, position=pos)
            else:
                break

        return node

    def _parse_unary(self) -> ASTNode:
        """Разбор унарных операторов."""
        if self.current_token and self.current_token.type == TokenType.OPERATOR:
            if self.current_token.value in ('+', '-'):
                op = self.current_token.value
                pos = self.current_token.position
                self._advance()
                operand = self._parse_unary()
                return UnaryOpNode(operator=op, operand=operand, position=pos)

        return self._parse_postfix()

    def _parse_postfix(self) -> ASTNode:
        """Разбор постфиксных операторов (унарный процент)."""
        node = self._parse_primary()

        if self.current_token and self.current_token.type == TokenType.PERCENT_SUFFIX:
            pos = self.current_token.position
            self._advance()
            node = PercentNode(operand=node, position=pos)

        return node

    def _parse_primary(self) -> ASTNode:
        """Разбор первичных конструкций."""
        if not self.current_token:
            raise ParseError("unexpected end of expression", 0)

        token = self.current_token

        if token.type == TokenType.NUMBER:
            self._advance()
            return NumberNode(value=float(token.value), position=token.position)

        if token.type == TokenType.IDENTIFIER:
            if (
                self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1].type == TokenType.LPAREN
            ):
                return self._parse_function_call()
            else:
                self._advance()
                return VariableNode(name=str(token.value), position=token.position)

        if token.type == TokenType.LPAREN:
            self._paren_count += 1
            self._advance()
            node = self._parse_expression()
            self._consume(TokenType.RPAREN)
            self._paren_count -= 1
            return node

        raise ParseError(f"unexpected token '{token.value}'", token.position)

    def _parse_function_call(self) -> FunctionCallNode:
        """Разбор вызова функции."""
        name_token = self._consume(TokenType.IDENTIFIER)
        name = str(name_token.value)
        pos = name_token.position

        self._consume(TokenType.LPAREN)
        self._paren_count += 1

        args: List[ASTNode] = []
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            args.append(self._parse_expression())
            while self.current_token and self.current_token.type == TokenType.COMMA:
                self._consume(TokenType.COMMA)
                args.append(self._parse_expression())

        self._consume(TokenType.RPAREN)
        self._paren_count -= 1

        return FunctionCallNode(name=name, arguments=args, position=pos)

    def _parse_assignment(self) -> AssignmentNode:
        """Разбор присваивания."""
        var_token = self._consume(TokenType.IDENTIFIER)
        var_name = str(var_token.value)
        pos = var_token.position

        self._consume(TokenType.ASSIGN)

        expr = self._parse_expression()

        return AssignmentNode(variable=var_name, expression=expr, position=pos)

    def _peek_next(self) -> Optional[TokenType]:
        """Просмотр следующего токена без продвижения."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1].type
        return None

    def _advance(self) -> None:
        """Продвижение к следующему токену."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def _consume(self, expected_type: TokenType) -> Token:
        """Потребление токена ожидаемого типа."""
        if not self.current_token:
            raise ParseError(f"expected {expected_type.name}, got EOF", 0)

        if self.current_token.type != expected_type:
            raise ParseError(
                f"expected {expected_type.name}, got {self.current_token.type.name}",
                self.current_token.position
            )

        token = self.current_token
        self._advance()
        return token
