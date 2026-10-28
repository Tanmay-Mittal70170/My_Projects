import tkinter as tk
import turtle
import customtkinter as ctk

# ---------- Colors ----------
BG = "#0f172a"
CARD = "#1e293b"
BORDER = "#334155"
ACCENT = "#3b82f6"
ACCENT_HOVER = "#2563eb"
MUTED = "#cbd5e1"
GREEN = "#34d399"          # light green (correct answer)
RED = "#f87171"            # light red (wrong answer)
TEXT = "#f1f5f9"           # bright text
DARK_TEXT = "#0f172a"      # text on the green / red buttons
OPTION_BG = "#334155"      # option buttons
OPTION_HOVER = "#475569"

# ---------- Folder of this file ----------
# The question files are looked for in the same folder where new_quiz.py is saved,
# no matter from which folder the program is started.
try:
    file_path = __file__.replace("\\", "/")
except NameError:
    file_path = ""

if "/" in file_path:
    BASE_FOLDER = file_path.rsplit("/", 1)[0] + "/"
else:
    BASE_FOLDER = ""


# =====================================================
# Reading questions from Question1.txt, Question2.txt, ...
#
# File format:
#   line 1             -> the question
#   lines until "A."   -> the code (optional)
#   A. / B. / C. / D.  -> the four options
#   correct_answer=A   -> the right option
#
# The program looks for Question1.txt, Question2.txt, Question3.txt ...
# in the folder you run it from, and stops at the first missing number.
# =====================================================
def trim_blank_lines(lines):
    """Remove empty lines at the start and end (keeps the spaces of other lines)."""
    while len(lines) > 0 and lines[0].strip() == "":
        lines.pop(0)
    while len(lines) > 0 and lines[-1].strip() == "":
        lines.pop()
    return lines


def remove_common_indent(lines):
    """Remove the spaces that ALL lines share, so a pattern keeps its shape."""
    indent = None
    for line in lines:
        if line.strip() != "":
            spaces = len(line) - len(line.lstrip(" "))
            if indent is None or spaces < indent:
                indent = spaces
    if not indent:
        return lines
    return [line[indent:] for line in lines]


def option_start(line, letter):
    """If this line starts option `letter` (like "A." or "A)"), return its first line.
    The label is replaced by spaces, so the text stays in the same column."""
    stripped = line.lstrip()
    if stripped[:2] == letter + "." or stripped[:2] == letter + ")":
        prefix_length = len(line) - len(stripped) + 2
        return " " * prefix_length + line[prefix_length:]
    return None


def parse_question(text, filename):
    lines = text.splitlines()

    question_lines = []                       # everything before option A
    options = {"A": [], "B": [], "C": [], "D": []}
    found = []                                # option letters found so far
    answer_letter = ""
    current = ""                              # option we are reading right now

    for line in lines:
        clean = line.strip().replace(" ", "").lower()
        next_letter = "ABCD"[len(found)] if len(found) < 4 else ""
        first = option_start(line, next_letter) if next_letter != "" else None

        if clean.startswith("correct_answer="):          # correct_answer=A
            answer_letter = clean.split("=")[1].upper()
            current = ""
        elif first is not None:                          # A. / B. / C. / D.
            current = next_letter
            found.append(next_letter)
            options[current].append(first)
        elif len(found) == 0:                            # question and code part
            question_lines.append(line)
        elif current != "":                              # more lines of the same option
            options[current].append(line)

    if len(found) != 4:
        found_text = ", ".join(found) if found else "none"
        raise ValueError(
            filename + ": need four options A. B. C. D. in order, each on its own line "
            "(found: " + found_text + ")"
        )
    if answer_letter not in ("A", "B", "C", "D"):
        raise ValueError(filename + ": add a line like correct_answer=A at the end")

    question_lines = trim_blank_lines(question_lines)
    if len(question_lines) == 0:
        raise ValueError(filename + ": the question text is missing")

    # First line = question, the rest = code
    question = question_lines[0].strip()
    before_dot = question.split(".", 1)[0]
    if before_dot.lower().startswith("question") and before_dot[8:].strip().isdigit():
        question = question.split(".", 1)[1].strip()     # remove "Question 1."

    code = "\n".join(trim_blank_lines(question_lines[1:]))

    option_texts = []
    for letter in "ABCD":
        option_lines = trim_blank_lines(options[letter])
        option_texts.append("\n".join(remove_common_indent(option_lines)))

    return {
        "question": question,
        "code": code,
        "options": option_texts,
        "answer": option_texts["ABCD".index(answer_letter)],
    }


def load_questions():
    questions = []
    number = 1
    while True:
        filename = "Question" + str(number) + ".txt"
        try:
            with open(BASE_FOLDER + filename, "r", encoding="utf-8-sig") as file:
                text = file.read()
        except FileNotFoundError:
            break                                         # no more question files
        except UnicodeDecodeError:
            raise ValueError(filename + ": please save the file with UTF-8 encoding")

        questions.append(parse_question(text, filename))
        number += 1
    return questions


# =====================================================
# Main (login) window
# =====================================================
ctk.set_appearance_mode("dark")

Screen = ctk.CTk()
Screen.title("Python Quiz")
Screen.geometry("500x620")
Screen.resizable(False, False)
Screen.configure(fg_color=BG)

# ---------- Card ----------
card = ctk.CTkFrame(
    Screen,
    fg_color=CARD,
    corner_radius=20,
    border_width=1,
    border_color=BORDER,
)
card.pack(padx=40, pady=40, fill="both", expand=True)

# ---------- Turtle logo: writes the word "Python" ----------
canvas = tk.Canvas(card, width=300, height=90, bg=CARD, highlightthickness=0)
canvas.pack(pady=(25, 5))

turtle_screen = turtle.TurtleScreen(canvas)
turtle_screen.bgcolor(CARD)
turtle_screen.tracer(0)

t = turtle.RawTurtle(turtle_screen)
t.hideturtle()
t.penup()

logo_font = ("Segoe UI", 40, "bold")
word = "Python"
colors = ["#3b82f6", "#8b5cf6", "#06b6d4", "#f472b6", "#3b82f6", "#8b5cf6"]

# Step 1: write the whole word once, just to measure how wide it is
t.goto(0, -25)
t.write(word, move=True, font=logo_font)     # move=True moves the turtle to the end of the text
total_width = t.xcor()
t.clear()                                    # erase the measuring text

# Step 2: write each letter in its own color, starting so the word is centered
t.goto(-total_width / 2, -25)                # y = text baseline
for ch, color in zip(word, colors):
    t.pencolor(color)
    t.write(ch, move=True, font=logo_font)   # the turtle moves right after each letter

turtle_screen.update()

# ---------- Headings ----------
ctk.CTkLabel(
    card, text="Welcome Back", font=("Segoe UI", 28, "bold")
).pack(pady=(10, 0))

ctk.CTkLabel(
    card, text="Sign in to start the Python Quiz",
    font=("Segoe UI", 13), text_color=MUTED
).pack(pady=(0, 25))

# ---------- Entries ----------
entry_style = dict(
    width=280, height=42, corner_radius=10,
    fg_color=BG, border_color=BORDER, border_width=1,
    font=("Segoe UI", 14),
)

admin_entry = ctk.CTkEntry(card, placeholder_text="Admin name", **entry_style)
admin_entry.pack(pady=8)

password_entry = ctk.CTkEntry(card, placeholder_text="Password", show="*", **entry_style)
password_entry.pack(pady=8)

# ---------- Show password ----------
def toggle_password():
    password_entry.configure(show="" if show_var.get() else "*")

show_var = ctk.BooleanVar(value=False)
ctk.CTkCheckBox(
    card, text="Show password", variable=show_var, command=toggle_password,
    font=("Segoe UI", 12), text_color=MUTED,
    fg_color=ACCENT, hover_color=ACCENT_HOVER,
    checkbox_width=18, checkbox_height=18,
).pack(pady=(5, 10))

# ---------- Result message ----------
result_label = ctk.CTkLabel(card, text="", font=("Segoe UI", 13))
result_label.pack(pady=5)


# =====================================================
# Quiz window (opens after a successful login)
# =====================================================
def show_quiz_screen():
    quiz = ctk.CTkToplevel(Screen)
    quiz.title("Quiz")
    quiz.geometry("640x740")
    quiz.minsize(640, 600)
    quiz.maxsize(1500, 1000)
    quiz.configure(fg_color=BG)

    Screen.withdraw()                                    # hide the login window
    quiz.protocol("WM_DELETE_WINDOW", Screen.destroy)    # closing the quiz closes the app
    quiz.lift()
    quiz.focus()

    # ----- Load the questions -----
    try:
        questions = load_questions()
        error = (
            "Could not find this file:\n" + BASE_FOLDER + "Question1.txt\n\n"
            "Save Question1.txt, Question2.txt ... in the same folder as new_quiz.py "
            "and check the names (no .txt.txt)."
        )
    except ValueError as e:
        questions = []
        error = str(e)

    quiz_frame = ctk.CTkFrame(
        quiz, fg_color=CARD, corner_radius=20,
        border_width=1, border_color=BORDER,
    )
    quiz_frame.pack(padx=30, pady=20, fill="both", expand=True)

    if len(questions) == 0:
        ctk.CTkLabel(
            quiz_frame, text=error, font=("Segoe UI", 16),
            text_color=RED, wraplength=480
        ).pack(expand=True)
        return

    state = {"index": 0, "score": 0, "options": []}

    def pad(text):
        # Make every line the same length, so multi-line patterns keep their
        # shape even though button text is centered (needs a monospace font)
        lines = text.split("\n")
        width = max(len(line) for line in lines)
        return "\n".join(line.ljust(width) for line in lines)

    # ----- Widgets (created once) -----
    ctk.CTkLabel(
        quiz_frame, text="Python Quiz", font=("Segoe UI", 24, "bold")
    ).pack(pady=(20, 0))

    progress_label = ctk.CTkLabel(
        quiz_frame, text="", font=("Segoe UI", 13), text_color=MUTED
    )
    progress_label.pack(pady=(0, 12))

    question_label = ctk.CTkLabel(
        quiz_frame, text="", font=("Segoe UI", 16, "bold"), wraplength=520
    )
    question_label.pack(pady=(0, 10))

    code_label = ctk.CTkLabel(
        quiz_frame, text="", font=("Consolas", 13), text_color=TEXT,
        fg_color=BG, corner_radius=10, justify="left", anchor="w",
    )

    options_frame = ctk.CTkFrame(quiz_frame, fg_color="transparent")
    options_frame.pack(pady=5)

    option_buttons = []
    for i in range(4):
        btn = ctk.CTkButton(
            options_frame, text="", width=240, height=44, corner_radius=10,
            fg_color=OPTION_BG, hover_color=OPTION_HOVER,
            text_color=TEXT, text_color_disabled=TEXT,
            border_width=1, border_color=OPTION_HOVER,
            font=("Consolas", 13),
        )
        btn.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="nsew")
        option_buttons.append(btn)

    feedback_label = ctk.CTkLabel(quiz_frame, text="", font=("Segoe UI", 13))
    feedback_label.pack(pady=6)

    next_button = ctk.CTkButton(
        quiz_frame, text="Next", width=140, height=38,
        fg_color=ACCENT, hover_color=ACCENT_HOVER, state="disabled",
    )
    next_button.pack(pady=(0, 15))

    # ----- Logic -----
    def show_question():
        q = questions[state["index"]]
        state["options"] = q["options"]

        progress_label.configure(
            text="Question " + str(state["index"] + 1) + " of " + str(len(questions))
        )
        question_label.configure(text=q["question"])

        if q["code"] != "":
            code_label.configure(text=q["code"])
            code_label.pack(before=options_frame, padx=30, pady=(0, 12), fill="x")
        else:
            code_label.pack_forget()

        for btn, opt in zip(option_buttons, q["options"]):
            lines = opt.count("\n") + 1
            btn.configure(
                text=pad(opt), height=max(44, 18 * lines + 22),
                state="normal", fg_color=OPTION_BG,
                text_color=TEXT, text_color_disabled=TEXT,
                command=lambda o=opt: check_answer(o),
            )

        feedback_label.configure(text="")
        is_last = state["index"] == len(questions) - 1
        next_button.configure(text="Finish" if is_last else "Next", state="disabled")

    def check_answer(choice):
        correct = questions[state["index"]]["answer"]
        for btn, opt in zip(option_buttons, state["options"]):
            btn.configure(state="disabled")
            if opt == correct:
                btn.configure(fg_color=GREEN, text_color_disabled=DARK_TEXT)   # correct answer
            elif opt == choice:
                btn.configure(fg_color=RED, text_color_disabled=DARK_TEXT)     # wrong choice

        if choice == correct:
            state["score"] += 1
            feedback_label.configure(text="Correct!", text_color=GREEN)
        else:
            feedback_label.configure(text="Wrong answer", text_color=RED)
        next_button.configure(state="normal")

    def next_question():
        state["index"] += 1
        if state["index"] < len(questions):
            show_question()
        else:
            show_result()

    def show_result():
        for widget in quiz_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            quiz_frame, text="Quiz Complete", font=("Segoe UI", 28, "bold")
        ).pack(pady=(120, 10))
        ctk.CTkLabel(
            quiz_frame,
            text="Your score: " + str(state["score"]) + " / " + str(len(questions)),
            font=("Segoe UI", 20), text_color=ACCENT
        ).pack(pady=10)

    next_button.configure(command=next_question)
    show_question()


# ---------- Login logic ----------
def login(event=None):
    if admin_entry.get() == "Python_Quiz" and password_entry.get() == "Python@123":
        result_label.configure(text="Login successful", text_color=GREEN)
        Screen.after(800, show_quiz_screen)   # wait 0.8 seconds, then open the quiz
    else:
        result_label.configure(text="Invalid name or password", text_color=RED)

ctk.CTkButton(
    card, text="Login", width=280, height=44, corner_radius=10,
    font=("Segoe UI", 15, "bold"),
    fg_color=ACCENT, hover_color=ACCENT_HOVER,
    command=login,
).pack(pady=(10, 20))

Screen.bind("<Return>", login)  # press Enter to log in

Screen.mainloop()