# tests.py

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file
from functions.run_file import run_python_file


# class TestCalculator(unittest.TestCase):

#     def test_get_files_info(self):
#         tests = [
#             ("Test calculator", "calculator", ".",
#              '''- lorem.txt: file_size=28, is_dir=False
# - tests.py: file_size=1342, is_dir=False
# - main.py: file_size=575, is_dir=False
# - pkg: file_size=4096, is_dir=True'''),
#             ("Test calculator/pkg", "calculator", "pkg",
#              '''- calculator.py: file_size=1737, is_dir=False
# - morelorem.txt: file_size=26, is_dir=False
# - render.py: file_size=766, is_dir=False
# - __pycache__: file_size=4096, is_dir=True'''),
#             ("Test /bin", "calculator", "/bin", 'Error: Cannot list "/bin" as it is outside the permitted working directory'),
#             ("Test calculator/../", "calculator", "../", 'Error: Cannot list "../" as it is outside the permitted working directory'),
#             ("Test calculator/tests.py", "calculator", "tests.py", 'Error: "tests.py" is not a directory')
#         ]

#         for i, test in enumerate(tests):
#             print(f"Test {i+1}:\nName: {test[0]}")
#             working_directory, directory, expected = test[1:]
#             actual = get_files_info(working_directory, directory)
#             self.assertEqual(expected, actual)
    
#     def test_get_file_content(self):
#         tests = [
#             # ("Test lorem.txt", "calculator", "lorem.txt"),
#             ("Test calculator/main.py", "calculator", "main.py",
#              '''# main.py

# import sys
# from pkg.calculator import Calculator
# from pkg.render import render


# def main():
#     calculator = Calculator()
#     if len(sys.argv) <= 1:
#         print("Calculator App")
#         print('Usage: python main.py "<expression>"')
#         print('Example: python main.py "3 + 5"')
#         return

#     expression = " ".join(sys.argv[1:])
#     try:
#         result = calculator.evaluate(expression)
#         to_print = render(expression, result)
#         print(to_print)
#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     main()'''),
#             ("Test /bin/cat", "calculator", "/bin/cat", 'Error: Cannot list "/bin/cat" as it is outside the permitted working directory'),
#             ("Test calculator/pkg/calculator.py", "calculator", "pkg/calculator.py",
#              '''# calculator.py

# class Calculator:
#     def __init__(self):
#         self.operators = {
#             "+": lambda a, b: a + b,
#             "-": lambda a, b: a - b,
#             "*": lambda a, b: a * b,
#             "/": lambda a, b: a / b,
#         }
#         self.precedence = {
#             "+": 1,
#             "-": 1,
#             "*": 2,
#             "/": 2,
#         }

#     def evaluate(self, expression):
#         if not expression or expression.isspace():
#             return None
#         tokens = expression.strip().split()
#         return self._evaluate_infix(tokens)

#     def _evaluate_infix(self, tokens):
#         values = []
#         operators = []

#         for token in tokens:
#             if token in self.operators:
#                 while (
#                     operators
#                     and operators[-1] in self.operators
#                     and self.precedence[operators[-1]] >= self.precedence[token]
#                 ):
#                     self._apply_operator(operators, values)
#                 operators.append(token)
#             else:
#                 try:
#                     values.append(float(token))
#                 except ValueError:
#                     raise ValueError(f"invalid token: {token}")

#         while operators:
#             self._apply_operator(operators, values)

#         if len(values) != 1:
#             raise ValueError("invalid expression")

#         return values[0]

#     def _apply_operator(self, operators, values):
#         if not operators:
#             return

#         operator = operators.pop()
#         if len(values) < 2:
#             raise ValueError(f"not enough operands for operator {operator}")

#         b = values.pop()
#         a = values.pop()
#         values.append(self.operators[operator](a, b))'''),
#             ("Test calculator/pkg", "calculator", "pkg", 'Error: File not found or is not a regular file: "pkg"')
#         ]

#         for i, test in enumerate(tests):
#             print(f"Test {i+1}:\nName: {test[0]}")
#             working_directory, file_path, expected = test[1:]
#             actual = get_file_content(working_directory, file_path)
#             print(actual)
#             self.assertEqual(expected, actual)

    # def test_write_file(self):
    #     tests = [
    #         ("test writing to lorem.txt", "calculator", "lorem.txt", "wait, this isn't lorem ipsum", "Successfully wrote"),
    #         ("test writing to pkg/morelorem.txt", "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", "Successfully wrote"),
    #         ("test writing to /tmp/temp.txt", "calculator", "/tmp/temp.txt", "this should not be allowed", "Error:"),
    #         ("test writing to pkg", "calculator", "pkg", "should raise an error", "Error:")
    #     ]

    #     for i, test in enumerate(tests):
    #         print(f"Test {i+1}:\nName: {test[0]}")
    #         working_directory, file_path, content, expected = test[1:]
    #         actual = write_file(working_directory, file_path, content)
    #         print(actual)
    #         self.assertTrue(expected in actual)

def test():
    result = run_python_file("calculator", "main.py", "3 + 5")
    print(result)
    result = run_python_file("calculator", "tests.py")
    print(result)
    result = run_python_file("calculator", "../main.py")
    print(result)
    result = run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == "__main__":
    test()