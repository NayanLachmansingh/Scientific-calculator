import tkinter as tk

from scientific_calculator import calculate


root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("460x800")
root.resizable(False, False)
root.configure(bg="#eef1f5")

equation = tk.StringVar(value="")
screen_expression = tk.StringVar(value="0")
screen_result = tk.StringVar(value="")
angle_mode = tk.StringVar(value="DEG")
history = []
memory = {"value": 0, "answer": None}

BASIC_BUTTONS = [
    ["C", "±", "%", "÷"], ["7", "8", "9", "×"],
    ["4", "5", "6", "−"], ["1", "2", "3", "+"],
    ["DEL", "0", ".", "="],
]
SCIENTIFIC_BUTTONS = [
    ["sin", "cos", "tan", "sin⁻¹"],
    ["cos⁻¹", "tan⁻¹", "sinh", "cosh"],
    ["tanh", "asinh", "acosh", "atanh"],
    ["log", "ln", "log₂", "eˣ"],
    ["10ˣ", "√", "∛", "x²"],
    ["xʸ", "1/x", "abs", "!"],
    ["%", "quad", "floor", "ceil"],
    ["π", "e", "mod", "("],
    [")", "MC", "MR", "M+"],
    ["M−", "Ans", "nCr", "nPr"],
    [",", "rand", "round"],
]

COLORS = {"panel": "#202938", "button": "#344154", "scientific": "#46546b",
          "operator": "#5268e8", "hover": "#7588ff"}
KEYS = {
    "÷": ("/", "÷"), "×": ("*", "×"), "−": ("-", "−"),
    "sin": ("sin(", "sin("), "cos": ("cos(", "cos("), "tan": ("tan(", "tan("),
    "sin⁻¹": ("asin(", "sin⁻¹("), "cos⁻¹": ("acos(", "cos⁻¹("),
    "tan⁻¹": ("atan(", "tan⁻¹("), "sinh": ("sinh(", "sinh("),
    "cosh": ("cosh(", "cosh("), "tanh": ("tanh(", "tanh("),
    "asinh": ("asinh(", "asinh("), "acosh": ("acosh(", "acosh("),
    "atanh": ("atanh(", "atanh("), "log": ("log10(", "log("),
    "ln": ("log(", "ln("), "log₂": ("log2(", "log₂("),
    "eˣ": ("exp(", "e^("), "10ˣ": ("pow10(", "10^("),
    "√": ("sqrt(", "√("), "∛": ("cbrt(", "∛("),
    "abs": ("abs(", "abs("), "floor": ("floor(", "floor("),
    "ceil": ("ceil(", "ceil("), "quad": ("quadratic_solver(", "quad("),
    "π": ("pi", "π"), "e": ("e", "e"), "mod": ("%", "mod"),
    "rand": ("random(", "rand("), "round": ("round(", "round("),
}

panel = tk.Frame(root, bg=COLORS["panel"], padx=20, pady=20)
panel.pack(padx=25, pady=20, fill="both", expand=True)
display = tk.Frame(panel, bg="#f8fafc", height=120)
display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 18))
display.grid_propagate(False)

tk.Label(display, text="SCIENTIFIC CALCULATOR", bg="#f8fafc", fg="#64748b",
         font=("Arial", 14), anchor="w").pack(fill="x", padx=16, pady=(10, 0))
tk.Label(display, textvariable=screen_expression, bg="#f8fafc", fg="#172033",
         font=("Arial", 22), anchor="e", wraplength=360).pack(
             fill="x", padx=16, pady=(4, 0))
tk.Label(display, textvariable=screen_result, bg="#f8fafc", fg="#5268e8",
         font=("Arial", 17), anchor="e").pack(fill="x", padx=16, pady=(0, 8))


def operand_start(text):
    if not text:
        return None
    end = len(text)
    if text.endswith("²"):
        return operand_start(text[:-1])
    if text.endswith("!"):
        start = operand_start(text[:-1])
        return start
    start = end - 1
    if text[start] == ")":
        depth = 1
        start -= 1
        while start >= 0 and depth:
            depth += (text[start] == ")") - (text[start] == "(")
            start -= 1
        if depth:
            return None
        start += 1
        while start and text[start - 1].isalpha():
            start -= 1
    elif text[start].isdigit() or text[start] == ".":
        while start and (text[start - 1].isdigit() or text[start - 1] == "."):
            start -= 1
    elif text[start].isalpha():
        while start and text[start - 1].isalpha():
            start -= 1
    else:
        return None
    if start and text[start - 1] in "-−" and (
        start == 1 or text[start - 2] in "+-*/%×÷−("
    ):
        start -= 1
    return start


def has_value(text):
    start = operand_start(text)
    return start is not None and (text[-1].isdigit() or text[-1] in ")!²" or text[start:] in ("pi", "e"))


def toggle_sign(text, sign):
    start = operand_start(text)
    if start is None:
        return text + sign
    if text[start] == sign:
        return text[:start] + text[start + 1:]
    return text[:start] + sign + text[start:]


def replace_last(expression, shown, function, display_function, close=True):
    start, shown_start = operand_start(expression), operand_start(shown)
    if start is None or shown_start is None:
        return expression, shown
    end = ")" if close else ","
    shown_end = ")" if close else ","
    return (
        expression[:start] + function + "(" + expression[start:] + end,
        shown[:shown_start] + display_function + "(" + shown[shown_start:] + shown_end,
    )


def append_power(expression, shown, power, symbol):
    start, shown_start = operand_start(expression), operand_start(shown)
    if start is None:
        return expression, shown
    base, shown_base = expression[start:], shown[shown_start:]
    if base.startswith("-"):
        base = "(" + base + ")"
    if shown_base.startswith("−"):
        shown_base = "(" + shown_base + ")"
    return expression[:start] + base + "**" + power, shown[:shown_start] + shown_base + symbol


def format_result(value):
    return format(value, ".12g") if isinstance(value, float) else str(value)


def show_button_press(label):
    current, shown = equation.get(), screen_expression.get()
    if not current:
        shown = ""

    if label == "C":
        current, shown = "", ""
        screen_result.set("")
        history.clear()
    elif label == "DEL":
        current, shown = history.pop() if history else ("", "")
        screen_result.set("")
    elif label == "=":
        if current:
            try:
                memory["answer"] = calculate(current, angle_mode.get())
                screen_result.set("= " + format_result(memory["answer"]))
            except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
                screen_result.set(str(error))
    elif label == "MC":
        memory["value"] = 0
        screen_result.set("Memory cleared")
    elif label in ("MR", "Ans"):
        value = memory["value"] if label == "MR" else memory["answer"]
        if value is None:
            screen_result.set("No stored answer yet.")
        else:
            history.append((current, shown))
            token = format_result(value)
            if has_value(current):
                current, shown = current + "*", shown + "×"
            current, shown = current + token, shown + token
            screen_result.set("")
    elif label in ("M+", "M−"):
        if current:
            try:
                value = calculate(current, angle_mode.get())
                memory["value"] += value if label == "M+" else -value
                screen_result.set("M = " + format_result(memory["value"]))
            except (ArithmeticError, SyntaxError, TypeError, ValueError) as error:
                screen_result.set(str(error))
    else:
        history.append((current, shown))
        screen_result.set("")
        if label == "±":
            current, shown = toggle_sign(current, "-"), toggle_sign(shown, "−")
        elif label == "!":
            start, shown_start = operand_start(current), operand_start(shown)
            if start is not None and shown_start is not None:
                current = current[:start] + "factorial(" + current[start:] + ")"
                shown += "!"
        elif label == "x²":
            current, shown = append_power(current, shown, "2", "²")
        elif label == "xʸ":
            current, shown = append_power(current, shown, "", "^")
        elif label == "1/x":
            current, shown = replace_last(current, shown, "reciprocal", "1/")
        elif label == "%":
            if has_value(current):
                current, shown = replace_last(current, shown, "percent", "")
                shown += "%"
        elif label in ("nCr", "nPr"):
            function = "combination" if label == "nCr" else "permutation"
            current, shown = replace_last(current, shown, function, label, close=False)
        else:
            value, symbol = KEYS.get(label, (label, label))
            start = operand_start(current)
            previous_is_constant = start is not None and current[start:] in ("pi", "e")
            add_multiply = has_value(current) and (
                label == "(" or label in ("π", "e") or value.endswith("(")
                or (label.isdigit() and (current.endswith(")") or previous_is_constant))
            )
            if add_multiply:
                current, shown = current + "*", shown + "×"
            current, shown = current + value, shown + symbol

    equation.set(current)
    screen_expression.set(shown or "0")


def make_button(parent, label, color, size, row, column):
    button = tk.Button(
        parent, text=label, command=lambda value=label: show_button_press(value),
        bg=color, fg="white", activebackground=COLORS["hover"],
        activeforeground="white", font=("Arial", size), relief="flat",
        borderwidth=0,
    )
    button.grid(row=row, column=column, padx=4, pady=3, sticky="nsew", ipady=8)
    button.original_color = color
    button.bind("<Enter>", lambda event: event.widget.configure(bg=COLORS["hover"]))
    button.bind("<Leave>", lambda event, original=color: event.widget.configure(bg=original))


def toggle_angle():
    angle_mode.set("RAD" if angle_mode.get() == "DEG" else "DEG")
    angle_button.configure(text=angle_mode.get())


for column in range(4):
    panel.grid_columnconfigure(column, weight=1)
for row, labels in enumerate(BASIC_BUTTONS, start=1):
    for column, label in enumerate(labels):
        color = "#18a879" if label == "=" else COLORS["operator"] if label in "÷×−+" else COLORS["button"]
        make_button(panel, label, color, 18, row, column)

tk.Label(panel, text="SCIENTIFIC FUNCTIONS", bg=COLORS["panel"], fg="#e2e8f0",
         font=("Arial", 13), anchor="w").grid(
             row=6, column=0, columnspan=3, sticky="ew", pady=(10, 4))
angle_button = tk.Button(panel, text=angle_mode.get(), command=toggle_angle,
                         bg=COLORS["operator"], fg="white", relief="flat")
angle_button.grid(row=6, column=3, sticky="ew", padx=4, pady=(10, 4))

area = tk.Frame(panel, bg=COLORS["panel"])
area.grid(row=7, column=0, columnspan=4, sticky="nsew")
canvas = tk.Canvas(area, bg=COLORS["panel"], highlightthickness=0, height=235)
scrollbar = tk.Scrollbar(area, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
buttons = tk.Frame(canvas, bg=COLORS["panel"])
window = canvas.create_window((0, 0), window=buttons, anchor="nw")
buttons.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))

for row, labels in enumerate(SCIENTIFIC_BUTTONS):
    for column, label in enumerate(labels):
        make_button(buttons, label, COLORS["scientific"], 12, row, column)

root.mainloop()
