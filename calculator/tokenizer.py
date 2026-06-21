"""Лексер для математических выражений."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Union

from .exceptions import TokenizeError


class TokenType(Enum):
    """Типы токенов."""
    NUMBER = auto()
    IDENTIFIER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    PERCENT_SUFFIX = auto()
    EOF = auto()


@dataclass
class Token:
    """Токен с позицией в строке."""
    type: TokenType
    value: Union[str, float]
    position: int


class Lexer:
    """Лексер для разбора математических выражений."""

    def __init__(self, expression: str):
        self.expression = expression
        self.pos = 0
        self.length = len(expression)
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """Разбить выражение на токены."""
        self.tokens = []

        while self.pos < self.length:
            ch = self.expression[self.pos]

            # Пропускаем пробелы
            if ch.isspace():
                self.pos += 1
                continue

            # Числа (включая научную нотацию)
            if ch.isdigit() or (ch == '.' and self._is_number_start()):
                self._tokenize_number()
                continue

            # Идентификаторы
            if ch.isalpha() or ch == '_':
                self._tokenize_identifier()
                continue

            # Операторы и специальные символы
            if ch == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.pos))
                self.pos += 1
                continue

            if ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.pos))
                self.pos += 1
                continue

            if ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.pos))
                self.pos += 1
                continue

            if ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.pos))
                self.pos += 1
                continue

            if ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.pos))
                self.pos += 1
                continue

            # Многосимвольные операторы
            if ch in '*/%+-':
                self._tokenize_operator()
                continue

            # Неизвестный символ
            raise TokenizeError(f"unexpected character '{ch}'", self.pos)

        self.tokens.append(Token(TokenType.EOF, '', self.pos))
        return self.tokens

    def _is_number_start(self) -> bool:
        """Проверяет, начинается ли число с текущей позиции."""
        next_pos = self.pos + 1
        return next_pos < self.length and self.expression[next_pos].isdigit()

    def _tokenize_number(self) -> None:
        """Токенизация числа с поддержкой научной нотации и разделителей."""
        start = self.pos
        value_str = ""
        has_dot = False
        has_exp = False

        while self.pos < self.length:
            ch = self.expression[self.pos]

            if ch.isdigit():
                value_str += ch
                self.pos += 1
            elif ch == '.' and not has_dot and not has_exp:
                has_dot = True
                value_str += ch
                self.pos += 1
            elif ch == '_':
                # Разделитель тысяч (PEP 515)
                self.pos += 1
                continue
            elif ch in 'eE' and not has_exp:
                has_exp = True
                value_str += ch
                self.pos += 1
                # Проверяем знак экспоненты
                if self.pos < self.length and self.expression[self.pos] in '+-':
                    value_str += self.expression[self.pos]
                    self.pos += 1
            else:
                break

        # Проверка на . без цифр после
        if value_str == '.' or value_str.endswith('.'):
            raise TokenizeError("invalid number format", start)

        try:
            value = float(value_str)
        except ValueError:
            raise TokenizeError(f"invalid number '{value_str}'", start)

        self.tokens.append(Token(TokenType.NUMBER, value, start))

    def _tokenize_identifier(self) -> None:
        """Токенизация идентификатора."""
        start = self.pos
        value = ""

        while self.pos < self.length:
            ch = self.expression[self.pos]
            if ch.isalnum() or ch == '_':
                value += ch
                self.pos += 1
            else:
                break

        self.tokens.append(Token(TokenType.IDENTIFIER, value, start))

    def _tokenize_operator(self) -> None:
        """Токенизация оператора."""
        start = self.pos
        ch = self.expression[self.pos]

        # Двухсимвольные операторы
        if ch == '*' and self.pos + 1 < self.length and self.expression[self.pos + 1] == '*':
            self.tokens.append(Token(TokenType.OPERATOR, '**', start))
            self.pos += 2
            return

        if ch == '/' and self.pos + 1 < self.length and self.expression[self.pos + 1] == '/':
            self.tokens.append(Token(TokenType.OPERATOR, '//', start))
            self.pos += 2
            return

        # Обработка % (бинарный или унарный)
        if ch == '%':
            # Если предыдущий токен - число или закрывающая скобка
            if self.tokens and self.tokens[-1].type in (TokenType.NUMBER, TokenType.RPAREN):
                # Проверяем, есть ли после % число (тогда это бинарный оператор)
                next_pos = self.pos + 1
                while next_pos < self.length and self.expression[next_pos].isspace():
                    next_pos += 1
                if next_pos < self.length and (
                    self.expression[next_pos].isdigit() or self.expression[next_pos] == '('
                ):
                    # Это бинарный оператор %
                    self.tokens.append(Token(TokenType.OPERATOR, '%', start))
                    self.pos += 1
                    return
                else:
                    # Это унарный процент
                    self.tokens.append(Token(TokenType.PERCENT_SUFFIX, '%', start))
                    self.pos += 1
                    return
            else:
                # Это бинарный оператор %
                self.tokens.append(Token(TokenType.OPERATOR, '%', start))
                self.pos += 1
                return

        # Односимвольные операторы
        self.tokens.append(Token(TokenType.OPERATOR, ch, start))
        self.pos += 1
