# src/parser.py
from src.lexer import Lexer, Token

# --- Узлы Абстрактного Синтаксического Дерева (AST) ---

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VariableDeclarationNode(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class FunctionDeclarationNode(ASTNode):
    def __init__(self, identifier, params, body):
        self.identifier = identifier
        self.params = params
        self.body = body

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class CallNode(ASTNode):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = float(token.value) if '.' in token.value else int(token.value)

class StringNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value[1:-1] # Убираем кавычки

class BooleanNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = True if token.value == 'истина' else False

class IdentifierNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

# --- Парсер ---

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        if self.tokens:
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def advance(self):
        """ Переход к следующему токену """
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """ Главный метод парсинга """
        statements = []
        while self.current_token is not None:
            if self.current_token.type == 'НОВАЯ_СТРОКА':
                self.advance()
                continue
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self):
        """ Парсинг одного выражения """
        if self.current_token.type == 'ПЕРЕМЕННАЯ':
            node = self.parse_variable_declaration()
        else:
            node = self.parse_expression()

        # Пропускаем новую строку после выражения
        if self.current_token and self.current_token.type == 'НОВАЯ_СТРОКА':
            self.advance()
        return node

    def parse_variable_declaration(self):
        """ Парсинг объявления переменной """
        self.advance() # Пропускаем 'переменная'
        identifier = IdentifierNode(self.current_token)
        self.advance() # Пропускаем идентификатор

        if self.current_token.type != 'ПРИСВАИВАНИЕ':
            raise SyntaxError("Ожидался символ '=' после имени переменной")
        self.advance() # Пропускаем '='

        value = self.parse_expression()
        return VariableDeclarationNode(identifier, value)

    def parse_expression(self):
        """ Парсинг выражения с бинарными операциями """
        node = self.parse_term()

        while self.current_token is not None and self.current_token.type in ('СЛОЖЕНИЕ', 'ВЫЧИТАНИЕ'):
            op_token = self.current_token
            self.advance()
            right_node = self.parse_term()
            node = BinaryOpNode(left=node, op=op_token, right=right_node)

        return node

    def parse_term(self):
        """ Парсинг терма (число, строка, идентификатор, вызов функции) """
        token = self.current_token

        if token.type == 'ЧИСЛО':
            self.advance()
            return NumberNode(token)
        elif token.type == 'СТРОКА':
            self.advance()
            return StringNode(token)
        elif token.type in ('ИСТИНА', 'ЛОЖЬ'):
            self.advance()
            return BooleanNode(token)
        elif token.type == 'ИДЕНТИФИКАТОР' or token.type == 'ВЫВОД':
            identifier_token = token
            self.advance()
            if self.current_token is not None and self.current_token.type == 'Л_СКОБКА':
                return self.parse_function_call(identifier_token)
            return IdentifierNode(identifier_token)

        raise SyntaxError(f"Неожиданный токен: {token}")

    def parse_function_call(self, identifier_token):
        """ Парсинг вызова функции """
        self.advance() # Пропускаем '('
        args = []
        if self.current_token.type != 'П_СКОБКА':
            args.append(self.parse_expression())
            # TODO: Добавить поддержку нескольких аргументов через запятую

        if self.current_token.type != 'П_СКОБКА':
            raise SyntaxError("Ожидалась ')' после аргументов функции")

        self.advance() # Пропускаем ')'
        return CallNode(callee=IdentifierNode(identifier_token), args=args)


if __name__ == '__main__':
    # Пример использования
    test_code = """
    переменная x = 10 + 5
    вывод(x)
    """
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    # Вывод AST для проверки (упрощенный)
    for stmt in ast.statements:
        print(stmt)
