# src/lexer.py
import re

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_pos = 0
        self.current_line = 1

    def tokenize(self):
        # Словарь с регулярными выражениями для токенов
        token_regexes = {
            'ЧИСЛО':      r'\d+(\.\d*)?',
            'СТРОКА':     r'"[^"]*"',
            'ПЕРЕМЕННАЯ': r'переменная',
            'ФУНКЦИЯ':    r'функция',
            'ЕСЛИ':       r'если',
            'ИНАЧЕ_ЕСЛИ': r'иначе если',
            'ИНАЧЕ':      r'иначе',
            'ПОКА':       r'пока',
            'ИСТИНА':     r'истина',
            'ЛОЖЬ':       r'ложь',
            'ВЫВОД':      r'вывод',
            'ИДЕНТИФИКАТОР': r'[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*',
            'ПРИСВАИВАНИЕ': r'=',
            'СЛОЖЕНИЕ':   r'\+',
            'ВЫЧИТАНИЕ':  r'-',
            'УМНОЖЕНИЕ':  r'\*',
            'ДЕЛЕНИЕ':    r'/',
            'РАВНО':      r'==',
            'НЕ_РАВНО':   r'!=',
            'МЕНЬШЕ_ИЛИ_РАВНО': r'<=',
            'БОЛЬШЕ_ИЛИ_РАВНО': r'>=',
            'МЕНЬШЕ':     r'<',
            'БОЛЬШЕ':     r'>',
            'Л_СКОБКА':   r'\(',
            'П_СКОБКА':   r'\)',
            'ДВОЕТОЧИЕ':  r':',
            'НОВАЯ_СТРОКА': r'\n',
            'ПРОБЕЛ':     r'[ \t]+',
            'НЕИЗВЕСТНЫЙ': r'.',
        }

        # Объединяем все регулярные выражения в одно
        regex_parts = [f'(?P<{name}>{pattern})' for name, pattern in token_regexes.items()]
        full_regex = re.compile('|'.join(regex_parts))

        while self.current_pos < len(self.code):
            match = full_regex.match(self.code, self.current_pos)

            if match:
                token_type = match.lastgroup
                token_value = match.group(token_type)

                if token_type == 'НОВАЯ_СТРОКА':
                    self.current_line += 1
                elif token_type == 'ПРОБЕЛ':
                    # Игнорируем пробелы
                    pass
                elif token_type != 'НЕИЗВЕСТНЫЙ':
                    self.tokens.append(Token(token_type, token_value, self.current_line))

                self.current_pos = match.end()
            else:
                # Если ни одно правило не сработало, это ошибка
                raise SyntaxError(f"Неизвестный символ на строке {self.current_line}")

        return self.tokens

if __name__ == '__main__':
    # Пример использования
    test_code = """
    переменная x = 10
    функция тест(а):
        вывод(а + x)
    """
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
