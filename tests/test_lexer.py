# tests/test_lexer.py
import pytest
from src.lexer import Lexer, Token

def test_tokenize_variable_declaration():
    code = "переменная x = 10"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected_tokens = [
        Token('ПЕРЕМЕННАЯ', 'переменная', 1),
        Token('ИДЕНТИФИКАТОР', 'x', 1),
        Token('ПРИСВАИВАНИЕ', '=', 1),
        Token('ЧИСЛО', '10', 1),
    ]

    assert len(tokens) == len(expected_tokens)
    for i in range(len(tokens)):
        assert tokens[i].type == expected_tokens[i].type
        assert tokens[i].value == expected_tokens[i].value

def test_tokenize_string():
    code = 'переменная s = "привет"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    assert tokens[3].type == 'СТРОКА'
    assert tokens[3].value == '"привет"'

def test_tokenize_operators():
    code = "10 + 5 - 2"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    assert tokens[1].type == 'СЛОЖЕНИЕ'
    assert tokens[3].type == 'ВЫЧИТАНИЕ'

def test_tokenize_function_call():
    code = "вывод(x)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    expected_types = ['ВЫВОД', 'Л_СКОБКА', 'ИДЕНТИФИКАТОР', 'П_СКОБКА']

    assert [t.type for t in tokens] == expected_types
