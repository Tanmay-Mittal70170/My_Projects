import customtkinter as ctk
import tkinter as tk


# -----------------------------
# App Settings
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Calculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("400x550")
        self.resizable(False, False)

        self.expression = ""

        # -----------------------------
        # Display
        # -----------------------------
        self.display = ctk.CTkEntry(
            self,
            width=360,
            height=70,
            font=("Arial", 28),
            justify="right"
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=20, pady=30)

        # -----------------------------
        # Buttons
        # -----------------------------
        buttons = [
            ("C", 1, 0),
            ("⌫", 1, 1),
            ("(", 1, 2),
            (")", 1, 3),

            ("7", 2, 0),
            ("8", 2, 1),
            ("9", 2, 2),
            ("/", 2, 3),

            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("*", 3, 3),

            ("1", 4, 0),
            ("2", 4, 1),
            ("3", 4, 2),
            ("-", 4, 3),

            ("0", 5, 0),
            (".", 5, 1),
            ("=", 5, 2),
            ("+", 5, 3)
        ]

        for text, row, column in buttons:

            button = ctk.CTkButton(
                self,
                text=text,
                width=80,
                height=60,
                font=("Arial", 20),
                command=lambda value=text: self.button_click(value)
            )

            button.grid(
                row=row,
                column=column,
                padx=8,
                pady=8
            )

    # -----------------------------
    # Button Function
    # -----------------------------
    def button_click(self, value):

        if value == "C":
            self.expression = ""
            self.display.delete(0, tk.END)

        elif value == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

        elif value == "=":
            try:
                result = eval(self.expression)

                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))

                self.expression = str(result)

            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
                self.expression = ""

        else:
            self.expression += value

            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()