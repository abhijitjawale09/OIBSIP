import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

# ─── PASSWORD LOGIC ───────────────────────────────────────────
def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    charset = ""
    guaranteed = []

    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = chars.replace("O", "").replace("I", "")
        charset += chars
        guaranteed.append(secrets.choice(chars))

    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = chars.replace("l", "")
        charset += chars
        guaranteed.append(secrets.choice(chars))

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = chars.replace("0", "").replace("1", "")
        charset += chars
        guaranteed.append(secrets.choice(chars))

    if use_symbols:
        chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        charset += chars
        guaranteed.append(secrets.choice(chars))

    if not charset:
        return None

    remaining = [secrets.choice(charset) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)

def check_strength(password):
    length = len(password)
    has_upper  = any(c.isupper() for c in password)
    has_lower  = any(c.islower() for c in password)
    has_digit  = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password)
    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length < 8 or score <= 1:
        return "Weak", "#e74c3c", 0.25
    elif length < 12 or score == 2:
        return "Medium", "#f39c12", 0.55
    elif length < 16 or score == 3:
        return "Strong", "#2ecc71", 0.80
    else:
        return "Very Strong", "#89b4fa", 1.0

# ─── MAIN APP ─────────────────────────────────────────────────
class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator — OIBSIP")
        self.root.geometry("520x680")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        self.history = []
        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root, text="🔐 Password Generator",
                 font=("Helvetica", 22, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=20)

        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(padx=40, fill="x")

        # Length Slider
        tk.Label(frame, text="Password Length",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(10,2))

        self.length_var = tk.IntVar(value=16)
        slider_frame = tk.Frame(frame, bg="#1e1e2e")
        slider_frame.pack(fill="x")

        self.length_label = tk.Label(slider_frame, text="16",
                                      font=("Helvetica", 12, "bold"),
                                      bg="#1e1e2e", fg="#89b4fa", width=3)
        self.length_label.pack(side="right")

        slider = tk.Scale(slider_frame, from_=8, to=64,
                          orient="horizontal", variable=self.length_var,
                          bg="#1e1e2e", fg="#cdd6f4",
                          highlightthickness=0, troughcolor="#313244",
                          activebackground="#89b4fa",
                          command=self.update_length_label)
        slider.pack(fill="x", side="left", expand=True)

        # Checkboxes
        tk.Label(frame, text="Character Types",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(15,5))

        self.use_upper   = tk.BooleanVar(value=True)
        self.use_lower   = tk.BooleanVar(value=True)
        self.use_digits  = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.excl_ambig  = tk.BooleanVar(value=False)

        checks = [
            ("Uppercase Letters (A-Z)", self.use_upper,   "#cdd6f4"),
            ("Lowercase Letters (a-z)", self.use_lower,   "#cdd6f4"),
            ("Numbers (0-9)",           self.use_digits,  "#cdd6f4"),
            ("Symbols (!@#$...)",       self.use_symbols, "#cdd6f4"),
            ("Exclude Ambiguous (0,O,l,1)", self.excl_ambig, "#f38ba8"),
        ]
        for text, var, color in checks:
            tk.Checkbutton(frame, text=text, variable=var,
                           font=("Helvetica", 11),
                           bg="#1e1e2e", fg=color,
                           selectcolor="#313244",
                           activebackground="#1e1e2e").pack(anchor="w", pady=2)

        # Generate Button
        tk.Button(frame, text="Generate Password",
                  font=("Helvetica", 13, "bold"),
                  bg="#89b4fa", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.generate).pack(fill="x", pady=20, ipady=10)

        # Password Display
        self.password_var = tk.StringVar()
        pwd_frame = tk.Frame(frame, bg="#313244")
        pwd_frame.pack(fill="x")

        self.pwd_entry = tk.Entry(pwd_frame, textvariable=self.password_var,
                                   font=("Courier", 13),
                                   bg="#313244", fg="#a6e3a1",
                                   insertbackground="white",
                                   relief="flat", state="readonly")
        self.pwd_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=10)

        tk.Button(pwd_frame, text="📋 Copy",
                  font=("Helvetica", 10),
                  bg="#a6e3a1", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.copy_password).pack(side="right", padx=5, pady=5, ipadx=5)

        # Strength Bar
        tk.Label(frame, text="Strength",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(15,2))

        self.strength_label = tk.Label(frame, text="",
                                        font=("Helvetica", 11, "bold"),
                                        bg="#1e1e2e", fg="#cdd6f4")
        self.strength_label.pack(anchor="w")

        self.canvas = tk.Canvas(frame, height=12, bg="#313244",
                                highlightthickness=0)
        self.canvas.pack(fill="x", pady=5)

        # History
        tk.Label(frame, text="Last 5 Passwords",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(15,5))

        self.history_frame = tk.Frame(frame, bg="#1e1e2e")
        self.history_frame.pack(fill="x")

    # ─── ACTIONS ──────────────────────────────────────────────
    def update_length_label(self, val):
        self.length_label.config(text=str(val))

    def generate(self):
        if not any([self.use_upper.get(), self.use_lower.get(),
                    self.use_digits.get(), self.use_symbols.get()]):
            messagebox.showerror("Error", "Select at least one character type.")
            return

        pwd = generate_password(
            self.length_var.get(),
            self.use_upper.get(),
            self.use_lower.get(),
            self.use_digits.get(),
            self.use_symbols.get(),
            self.excl_ambig.get()
        )

        if pwd:
            self.password_var.set(pwd)
            self.update_strength(pwd)
            self.update_history(pwd)

    def copy_password(self):
        pwd = self.password_var.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied!", "Password copied to clipboard ✅")
        else:
            messagebox.showerror("Error", "Generate a password first.")

    def update_strength(self, password):
        label, color, ratio = check_strength(password)
        self.strength_label.config(text=label, fg=color)
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        if width < 10:
            width = 440
        self.canvas.create_rectangle(0, 0, width * ratio, 12,
                                      fill=color, outline="")

    def update_history(self, pwd):
        self.history.insert(0, pwd)
        self.history = self.history[:5]
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        for p in self.history:
            tk.Label(self.history_frame,
                     text=p,
                     font=("Courier", 10),
                     bg="#313244", fg="#cdd6f4",
                     anchor="w", padx=8, pady=4).pack(fill="x", pady=1)

# ─── RUN ──────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()