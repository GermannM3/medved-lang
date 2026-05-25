#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Медведь - язык программирования на кириллице
Минимальное ядро для запуска программ на языке Медведь
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from лексер import Лексер
from парсер import Парсер
from исполнитель import Исполнитель

def запустить(путь_к_файлу):
    """Запустить программу на языке Медведь"""
    if not os.path.exists(путь_к_файлу):
        print(f"Ошибка: файл '{путь_к_файлу}' не найден")
        return 1
    
    with open(путь_к_файлу, 'r', encoding='utf-8') as файл:
        код = файл.read()
    
    try:
        # Лексический анализ
        лексер = Лексер(код)
        токены = лексер.токенизировать()
        
        # Синтаксический анализ
        парсер = Парсер(токены)
        ast = парсер.разобрать()
        
        # Выполнение
        исполнитель = Исполнитель()
        исполнитель.выполнить(ast)
        
        return 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 главный.py <файл.мед>")
        print("Пример: python3 главный.py examples/привет.мед")
        sys.exit(1)
    
    путь = sys.argv[1]
    sys.exit(запустить(путь))
