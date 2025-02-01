# tests/test_compiler.py

import unittest
from src.compiler import компилировать_в_машинный_код

class TestCompiler(unittest.TestCase):
    def test_компилировать_в_машинный_код(self):
        код = "функция приветствие()"
        self.assertEqual(компилировать_в_машинный_код(код), "Машинный код для: функция приветствие()")

if __name__ == "__main__":
    unittest.main()

