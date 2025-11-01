# src/interpreter.py
from src.parser import (
    ASTNode, ProgramNode, VariableDeclarationNode, BinaryOpNode, CallNode,
    NumberNode, StringNode, BooleanNode, IdentifierNode
)
from src.lexer import Lexer
from src.parser import Parser

class Interpreter:
    def __init__(self):
        # Таблица символов для хранения переменных
        self.symbol_table = {
            'вывод': self.builtin_print  # Встроенная функция
        }

    def builtin_print(self, *args):
        """ Встроенная функция для вывода в консоль """
        print(*args)

    def visit(self, node):
        """ Динамический вызов метода visit_<тип_узла> """
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Обработчик для неизвестных узлов """
        raise Exception(f'Нет метода visit_{type(node).__name__}')

    def visit_ProgramNode(self, node):
        """ Обход корневого узла программы """
        for statement in node.statements:
            self.visit(statement)

    def visit_VariableDeclarationNode(self, node):
        """ Обработка объявления переменной """
        value = self.visit(node.value)
        self.symbol_table[node.identifier.value] = value
        return value

    def visit_BinaryOpNode(self, node):
        """ Обработка бинарных операций """
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op.type

        if op == 'СЛОЖЕНИЕ':
            return left + right
        elif op == 'ВЫЧИТАНИЕ':
            return left - right
        # Добавьте здесь другие операции

        raise TypeError(f"Неподдерживаемая операция: {op}")

    def visit_CallNode(self, node):
        """ Обработка вызова функции """
        callee_name = node.callee.value
        if callee_name not in self.symbol_table:
            raise NameError(f"Функция '{callee_name}' не определена")

        function = self.symbol_table[callee_name]

        args = [self.visit(arg) for arg in node.args]

        # Проверяем, является ли "функция" действительно вызываемой
        if callable(function):
            return function(*args)
        else:
            # Здесь будет логика для пользовательских функций
            raise TypeError(f"'{callee_name}' не является функцией")

    def visit_NumberNode(self, node):
        """ Возвращает числовое значение """
        return node.value

    def visit_StringNode(self, node):
        """ Возвращает строковое значение """
        return node.value

    def visit_BooleanNode(self, node):
        """ Возвращает булево значение """
        return node.value

    def visit_IdentifierNode(self, node):
        """ Получение значения переменной из таблицы символов """
        var_name = node.value
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]
        else:
            raise NameError(f"Переменная '{var_name}' не определена")

    def interpret(self, ast):
        """ Главный метод для запуска интерпретации """
        if not isinstance(ast, ASTNode):
            raise TypeError("На вход ожидался узел AST")
        return self.visit(ast)


if __name__ == '__main__':
    # Пример использования
    test_code = """
    переменная x = 15 + 5
    переменная y = x - 2
    вывод("Значение y:", y)
    """

    # 1. Лексер
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()

    # 2. Парсер
    parser = Parser(tokens)
    ast = parser.parse()

    # 3. Интерпретатор
    interpreter = Interpreter()
    interpreter.interpret(ast)

    print("\nТаблица символов:")
    print(interpreter.symbol_table)
