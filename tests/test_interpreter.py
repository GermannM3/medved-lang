# tests/test_interpreter.py
import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def test_interpret_variable_declaration():
    code = "переменная x = 42"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)

    assert 'x' in interpreter.symbol_table
    assert interpreter.symbol_table['x'] == 42

def test_interpret_binary_operation():
    code = "переменная y = 10 + 2"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)

    assert interpreter.symbol_table['y'] == 12

def test_interpret_function_call(capsys):
    code = 'вывод("привет")'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)

    captured = capsys.readouterr()
    assert captured.out.strip() == "привет"

def test_interpret_variable_lookup():
    code = """
    переменная a = 5
    переменная b = a + 10
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)

    assert interpreter.symbol_table['b'] == 15
