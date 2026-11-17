import ast
import math


__all__ = ["calculate"]


def calculate(expression):
    """Evaluate a calculator expression without executing arbitrary Python code."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter a calculation first.")

    tree = ast.parse(expression, mode="eval")
    return _calculate_node(tree.body)


def _calculate_node(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.Name):
        constants = {"pi": math.pi, "e": math.e}
        if node.id in constants:
            return constants[node.id]
        raise ValueError("That value is not available.")

    if isinstance(node, ast.BinOp):
        left = _calculate_node(node.left)
        right = _calculate_node(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise ValueError("Division by zero is not allowed.")
            return left / right
        if isinstance(node.op, ast.Mod):
            if right == 0:
                raise ValueError("Division by zero is not allowed.")
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right

    if isinstance(node, ast.UnaryOp):
        value = _calculate_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +value
        if isinstance(node.op, ast.USub):
            return -value

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.keywords:
            raise ValueError("That function is not available.")

        functions = {
            "sin": sine,
            "cos": cosine,
            "tan": tangent,
            "log10": math.log10,
            "log": math.log,
            "sqrt": square_root,
            "factorial": factorial,
            "addition": addition,
            "subtraction": subtraction,
            "multiplication": multiplication,
            "division": division,
            "exponentiation": exponentiation,
            "logarithm": logarithm,
            "square_root": square_root,
            "quadratic_solver": quadratic_solver,
            "sine": sine,
            "cosine": cosine,
            "tangent": tangent,
        }
        function = functions.get(node.func.id)
        if function is None:
            raise ValueError("That function is not available.")
        args = [_calculate_node(arg) for arg in node.args]
        return function(*args)

    raise ValueError("Please enter a valid calculation.")


def addition(a, b):
    return a + b


def subtraction(a, b):
    return a - b


def multiplication(a, b):
    return a * b


def division(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


def exponentiation(a, b):
    return a ** b


def logarithm(a, b):
    if a <= 0 or b <= 0 or b == 1:
        raise ValueError("Logarithm requires a positive value and a positive base other than 1.")
    return math.log(a, b)


def square_root(a):
    if a < 0:
        raise ValueError("Square root is only defined for non-negative numbers.")
    return math.sqrt(a)


def factorial(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("Factorial requires a non-negative integer.")
    return math.factorial(value)


def quadratic_solver(a, b, c):
    if a == 0:
        raise ValueError("The first quadratic coefficient cannot be zero.")
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    if discriminant == 0:
        return (-b / (2 * a),)
    root = math.sqrt(discriminant)
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))


def sine(angle):
    return math.sin(math.radians(angle))


def cosine(angle):
    return math.cos(math.radians(angle))


def tangent(angle):
    return math.tan(math.radians(angle))
