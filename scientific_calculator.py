import ast
import math


__all__ = ["calculate"]


def calculate(expression, angle_mode="DEG"):
    """Evaluate a calculator expression without executing arbitrary Python code."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter a calculation first.")
    if angle_mode not in ("DEG", "RAD"):
        raise ValueError("Angle mode must be DEG or RAD.")

    tree = ast.parse(expression, mode="eval")
    return _calculate_node(tree.body, angle_mode)


def _calculate_node(node, angle_mode):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.Name):
        constants = {"pi": math.pi, "e": math.e}
        if node.id in constants:
            return constants[node.id]
        raise ValueError("That value is not available.")

    if isinstance(node, ast.BinOp):
        left = _calculate_node(node.left, angle_mode)
        right = _calculate_node(node.right, angle_mode)

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
        value = _calculate_node(node.operand, angle_mode)
        if isinstance(node.op, ast.UAdd):
            return +value
        if isinstance(node.op, ast.USub):
            return -value

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.keywords:
            raise ValueError("That function is not available.")

        to_radians = math.radians if angle_mode == "DEG" else lambda value: value
        from_radians = math.degrees if angle_mode == "DEG" else lambda value: value
        functions = {
            "sin": lambda value: math.sin(to_radians(value)),
            "cos": lambda value: math.cos(to_radians(value)),
            "tan": lambda value: math.tan(to_radians(value)),
            "asin": lambda value: from_radians(math.asin(value)),
            "acos": lambda value: from_radians(math.acos(value)),
            "atan": lambda value: from_radians(math.atan(value)),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "asinh": math.asinh,
            "acosh": math.acosh,
            "atanh": math.atanh,
            "log10": math.log10,
            "log2": math.log2,
            "log": math.log,
            "sqrt": square_root,
            "cbrt": cube_root,
            "factorial": factorial,
            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,
            "exp": math.exp,
            "pow10": lambda value: 10 ** value,
            "percent": lambda value: value / 100,
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
        args = [_calculate_node(arg, angle_mode) for arg in node.args]
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


def cube_root(a):
    return math.copysign(abs(a) ** (1 / 3), a)


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
