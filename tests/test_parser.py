# tests/test_parser.py

import unittest
from src.parser import парсить_код

class TestParser(unittest.TestCase):
    def test_парсить_код(self):
        код = "функция приветствие()"
        self.assertEqual(парсить_код(код), "Парсинг: функция приветствие()")

if __name__ == "__main__":
    unittest.main()

