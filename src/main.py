# src/main.py
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
import sys

def запуск(код):
    """
    Выполняет полный цикл обработки кода:
    Лексер -> Парсер -> Интерпретатор
    """
    try:
        # 1. Лексический анализ (Токенизация)
        lexer = Lexer(код)
        tokens = lexer.tokenize()
        if not tokens:
            print("Нет токенов для обработки.")
            return

        # 2. Синтаксический анализ (Парсинг)
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. Исполнение (Интерпретация)
        interpreter = Interpreter()
        interpreter.interpret(ast)

    except (SyntaxError, NameError, TypeError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)

def запустить_файл(имя_файла):
    """
    Читает код из файла и запускает его.
    """
    try:
        with open(имя_файла, 'r', encoding='utf-8') as f:
            код = f.read()
        запуск(код)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{имя_файла}' не найден.", file=sys.stderr)

def интерактивный_режим():
    """
    Запускает интерактивную консоль (REPL).
    """
    print("Интерактивный режим 'Медведь'. Для выхода введите 'выход()'.")
    interpreter = Interpreter() # Создаем один интерпретатор на сессию

    while True:
        try:
            код = input(">>> ")
            if код.strip() == "выход()":
                break

            # В интерактивном режиме выполняем каждую строку
            lexer = Lexer(код)
            tokens = lexer.tokenize()
            if not tokens:
                continue

            parser = Parser(tokens)
            ast = parser.parse()

            # Интерпретируем в контексте текущей сессии
            interpreter.interpret(ast)

        except (SyntaxError, NameError, TypeError) as e:
            print(f"Ошибка: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Неожиданная ошибка: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Если передан аргумент командной строки, считаем его именем файла
        запустить_файл(sys.argv[1])
    else:
        # В противном случае запускаем интерактивный режим
        интерактивный_режим()
