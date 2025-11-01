# tests/test_parser.py
import pytest
from src.lexer import Lexer
from src.parser import Parser, VariableDeclarationNode, BinaryOpNode, NumberNode, CallNode

def test_parse_variable_declaration():
    code = "переменная x = 10"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    stmt = ast.statements[0]
    assert isinstance(stmt, VariableDeclarationNode)
    assert stmt.identifier.value == 'x'
    assert isinstance(stmt.value, NumberNode)
    assert stmt.value.value == 10

def test_parse_binary_operation():
    code = "15 + 5"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    expr = ast.statements[0]
    assert isinstance(expr, BinaryOpNode)
    assert expr.left.value == 15
    assert expr.op.type == 'СЛОЖЕНИЕ'
    assert expr.right.value == 5

def test_parse_function_call():
    code = "вывод(y)"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    expr = ast.statements[0]
    assert isinstance(expr, CallNode)
    assert expr.callee.value == 'вывод'
    assert len(expr.args) == 1
    assert expr.args[0].value == 'y'
