import unittest
from unittest import TestCase, main
import calculator


class test_calculator(TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(6, 4), 10)
        self.assertEqual(calculator.add(6, -4), 2)
        self.assertEqual(calculator.add(-6, 4), -2)
        self.assertEqual(calculator.add(-6, -4), -10)
        self.assertEqual(calculator.add(1.5, -4), -2.5)

    def test_multiply(self):
        self.assertEqual(calculator.add(6, 4), 10)
        self.assertEqual(calculator.add(6, -4), 2)
        self.assertEqual(calculator.add(-6, 4), -2)
        self.assertEqual(calculator.add(-6, -4), -10)

    def test_subtract(self):
        self.fail()

    def test_divide(self):
        self.assertRaises(ValueError, calculator.divide, 4, 0)
        self.fail()


if __name__ == "__main__":
    unittest.main()
