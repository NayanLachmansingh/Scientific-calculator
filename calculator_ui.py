import tkinter as tk

from scientific_calculator import calculate as calculate_expression


root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("460x800")
root.resizable(False, False)
root.configure(bg="#eef1f5")

equation = tk.StringVar(root, value="")
screen_expression = tk.StringVar(root, value="0")
screen_result = tk.StringVar(root, value="")
equation_history = []

panel = tk.Frame(root, bg="#202938", padx=20, pady=20)
panel.pack(padx=25, pady=20, fill="both", expand=True)

display = tk.Frame(panel, bg="#f8fafc", height=120)
display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 18))
display.grid_propagate(False)

title = tk.Label(
    display, text="SCIENTIFIC CALCULATOR", bg="#f8fafc", fg="#64748b",
    font=("Arial", 14), anchor="w",
)
title.pack(fill="x", padx=16, pady=(10, 0))

expression_label = tk.Label(
    display, textvariable=screen_expression, bg="#f8fafc", fg="#172033",
    font=("Arial", 22), anchor="e", wraplength=360,
)
expression_label.pack(fill="x", padx=16, pady=(4, 0))

result_label = tk.Label(
    display, textvariable=screen_result, bg="#f8fafc", fg="#5268e8",
    font=("Arial", 17), anchor="e",
)
result_label.pack(fill="x", padx=16, pady=(0, 8))

basic_buttons = [
    ["C", "±", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["DEL", "0", ".", "="],
]

scientific_buttons = [
    ["sin", "cos", "tan", "log"],
    ["ln", "√", "x²", "xʸ"],
    ["π", "(", ")", "!"],
]

operator_color = "#5268e8"
basic_color = "#344154"
scientific_color = "#46546b"
hover_color = "#7588ff"


def get_equation():
    return equation.get()


def last_operand_start(expression):
    if not expression:
        return None

    start = len(expression) - 1
    if expression[start] == ")":
        depth = 1
        start -= 1
        while start >= 0 and depth:
            if expression[start] == ")":
                depth += 1
            elif expression[start] == "(":
                depth -= 1
            start -= 1
        if depth:
            return None
        start += 1
        while start > 0 and expression[start - 1].isalpha():
            start -= 1
    elif expression[start].isdigit() or expression[start] == ".":
        while start > 0 and (expression[start - 1].isdigit() or expression[start - 1] == "."):
            start -= 1
    elif expression[start].isalpha():
        while start > 0 and expression[start - 1].isalpha():
            start -= 1
    else:
        return None
    return start


def append_factorial(expression):
    start = last_operand_start(expression)
    if start is None:
        return expression + "factorial("
    return expression[:start] + "factorial(" + expression[start:] + ")"


def toggle_sign(expression, sign="-"):
    start = last_operand_start(expression)
    if start is None:
        return expression + sign
    if start > 0 and expression[start - 1] == sign and (
        start == 1 or expression[start - 2] in "+-*/%("
    ):
        return expression[:start - 1] + expression[start:]
    return expression[:start] + sign + expression[start:]


def append_power(expression, shown, exponent, display_exponent):
    start = last_operand_start(expression)
    if start is None:
        return expression, shown

    if start > 0 and expression[start - 1] == "-" and (
        start == 1 or expression[start - 2] in "+-*/%("
    ):
        start -= 1
        expression = expression[:start] + "(" + expression[start:] + ")"
        shown_start = last_operand_start(shown)
        if shown_start is not None and shown_start > 0 and shown[shown_start - 1] == "−" and (
            shown_start == 1 or shown[shown_start - 2] in "+-*/%×÷−("
        ):
            shown_start -= 1
            shown = shown[:shown_start] + "(" + shown[shown_start:] + ")"

    return expression + "**" + exponent, shown + display_exponent


def format_result(value):
    if isinstance(value, float):
        return format(value, ".12g")
    return str(value)


def calculate_for_display(expression):
    try:
        return "= " + format_result(calculate_expression(expression))
    except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
        return str(error)


def show_button_press(label):
    current = get_equation()
    shown = screen_expression.get()
    if not current:
        shown = ""

    if label == "C":
        current = ""
        shown = ""
        screen_result.set("")
        equation_history.clear()
    elif label == "DEL":
        if equation_history:
            current, shown = equation_history.pop()
        else:
            current = ""
            shown = ""
        screen_result.set("")
    elif label == "=":
        if current:
            screen_result.set(calculate_for_display(current))
    else:
        equation_history.append((current, shown))
        screen_result.set("")
        if label == "±":
            current = toggle_sign(current)
            shown = toggle_sign(shown, "−")
        elif label == "!":
            current = append_factorial(current)
            shown += "!"
        elif label == "x²":
            current, shown = append_power(current, shown, "2", "²")
        elif label == "xʸ":
            current, shown = append_power(current, shown, "", "^")
        else:
            button_values = {
                "÷": "/",
                "×": "*",
                "−": "-",
                "sin": "sin(",
                "cos": "cos(",
                "tan": "tan(",
                "log": "log10(",
                "ln": "log(",
                "√": "sqrt(",
                "π": "pi",
            }
            current += button_values.get(label, label)
            shown += label

    equation.set(current)
    screen_expression.set(shown or "0")


def highlight_button(event):
    event.widget.configure(bg=hover_color)


def restore_button_color(event):
    button = event.widget
    button.configure(bg=button.original_color, fg=button.original_text_color)


def create_button(parent, label, color, font_size, row, column):
    button = tk.Button(
        parent,
        text=label,
        bg=color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        font=("Arial", font_size),
        relief="flat",
        borderwidth=0,
        command=lambda value=label: show_button_press(value),
    )
    button.grid(row=row, column=column, padx=4, pady=3, sticky="nsew", ipady=8)
    button.original_color = color
    button.original_text_color = "white"
    button.bind("<Enter>", highlight_button)
    button.bind("<Leave>", restore_button_color)


for column in range(4):
    panel.grid_columnconfigure(column, weight=1)

for row, labels in enumerate(basic_buttons, start=1):
    for column, label in enumerate(labels):
        color = basic_color
        if label == "=":
            color = "#18a879"
        elif label in ["÷", "×", "−", "+"]:
            color = operator_color
        create_button(panel, label, color, 18, row, column)

scientific_title = tk.Label(
    panel, text="SCIENTIFIC FUNCTIONS", bg="#202938", fg="#e2e8f0",
    font=("Arial", 13), anchor="w",
)
scientific_title.grid(row=6, column=0, columnspan=4, sticky="ew", pady=(10, 4))

for row, labels in enumerate(scientific_buttons, start=7):
    for column, label in enumerate(labels):
        create_button(panel, label, scientific_color, 14, row, column)

root.mainloop()
