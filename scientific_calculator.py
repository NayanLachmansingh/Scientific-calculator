import ast
import math
import operator
import random


__all__ = ["calculate"]

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression, angle_mode="DEG"):
    """Evaluate an expression made from calculator buttons."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter a calculation first.")
    if angle_mode not in ("DEG", "RAD"):
        raise ValueError("Angle mode must be DEG or RAD.")

    tree = ast.parse(expression, mode="eval")
    return _evaluate(tree.body, _functions(angle_mode))


def _functions(angle_mode):
    to_radians = math.radians if angle_mode == "DEG" else lambda value: value
    from_radians = math.degrees if angle_mode == "DEG" else lambda value: value
    return {
        "sin": lambda value: math.sin(to_radians(value)),
        "cos": lambda value: math.cos(to_radians(value)),
        "tan": lambda value: math.tan(to_radians(value)),
        "asin": lambda value: from_radians(math.asin(value)),
        "acos": lambda value: from_radians(math.acos(value)),
        "atan": lambda value: from_radians(math.atan(value)),
        "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
        "asinh": math.asinh, "acosh": math.acosh, "atanh": math.atanh,
        "log10": math.log10, "log2": math.log2, "log": math.log,
        "sqrt": square_root, "cbrt": cube_root, "factorial": factorial,
        "reciprocal": reciprocal, "abs": abs, "floor": math.floor,
        "ceil": math.ceil, "exp": math.exp, "pow10": lambda value: 10 ** value,
        "percent": lambda value: value / 100, "combination": combination,
        "permutation": permutation, "random": random.random, "round": round,
        "addition": operator.add, "subtraction": operator.sub,
        "multiplication": operator.mul, "division": divide,
        "exponentiation": operator.pow, "logarithm": logarithm,
        "square_root": square_root, "quadratic_solver": quadratic_solver,
        "sine": sine, "cosine": cosine, "tangent": tangent,
    }


def _evaluate(node, functions):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in ("pi", "e"):
            return getattr(math, node.id)
        raise ValueError("That value is not available.")
    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Please enter a valid calculation.")
        left, right = _evaluate(node.left, functions), _evaluate(node.right, functions)
        if isinstance(node.op, (ast.Div, ast.Mod)) and right == 0:
            raise ValueError("Division by zero is not allowed.")
        return operation(left, right)
    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Please enter a valid calculation.")
        return operation(_evaluate(node.operand, functions))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        function = functions.get(node.func.id)
        if function is None or node.keywords:
            raise ValueError("That function is not available.")
        return function(*(_evaluate(arg, functions) for arg in node.args))
    raise ValueError("Please enter a valid calculation.")


def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


def logarithm(value, base):
    if value <= 0 or base <= 0 or base == 1:
        raise ValueError("Logarithm requires a positive value and a positive base other than 1.")
    return math.log(value, base)


def square_root(value):
    if value < 0:
        raise ValueError("Square root is only defined for non-negative numbers.")
    return math.sqrt(value)


def cube_root(value):
    return math.copysign(abs(value) ** (1 / 3), value)


def reciprocal(value):
    return divide(1, value)


def factorial(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("Factorial requires a non-negative integer.")
    return math.factorial(value)


def combination(n, r):
    if not isinstance(n, int) or not isinstance(r, int) or n < 0 or r < 0 or r > n:
        raise ValueError("Combination requires integers with 0 <= r <= n.")
    return math.comb(n, r)


def permutation(n, r):
    if not isinstance(n, int) or not isinstance(r, int) or n < 0 or r < 0 or r > n:
        raise ValueError("Permutation requires integers with 0 <= r <= n.")
    return math.perm(n, r)


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
