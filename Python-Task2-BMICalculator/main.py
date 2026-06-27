import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# ─── DATABASE SETUP ───────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_record(name, weight, height, bmi, category):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bmi_records (name, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_records(name):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, bmi, category FROM bmi_records
        WHERE name = ? ORDER BY date ASC
    """, (name,))
    records = cursor.fetchall()
    conn.close()
    return records

# ─── BMI LOGIC ────────────────────────────────────────────────
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db"
    elif bmi < 25:
        return "Normal", "#2ecc71"
    elif bmi < 30:
        return "Overweight", "#f39c12"
    else:
        return "Obese", "#e74c3c"

# ─── MAIN APP ─────────────────────────────────────────────────
class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator — OIBSIP")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)
        init_db()
        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root, text="BMI Calculator",
                 font=("Helvetica", 22, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=20)

        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(padx=40, fill="x")

        # Name
        tk.Label(frame, text="Your Name",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(10,2))
        self.name_entry = tk.Entry(frame, font=("Helvetica", 12),
                                   bg="#313244", fg="#cdd6f4",
                                   insertbackground="white", relief="flat")
        self.name_entry.pack(fill="x", ipady=8)

        # Weight
        tk.Label(frame, text="Weight (kg)",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(10,2))
        self.weight_entry = tk.Entry(frame, font=("Helvetica", 12),
                                      bg="#313244", fg="#cdd6f4",
                                      insertbackground="white", relief="flat")
        self.weight_entry.pack(fill="x", ipady=8)

        # Height
        tk.Label(frame, text="Height (m)  e.g. 1.75",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack(anchor="w", pady=(10,2))
        self.height_entry = tk.Entry(frame, font=("Helvetica", 12),
                                      bg="#313244", fg="#cdd6f4",
                                      insertbackground="white", relief="flat")
        self.height_entry.pack(fill="x", ipady=8)

        # Calculate Button
        tk.Button(frame, text="Calculate BMI",
                  font=("Helvetica", 13, "bold"),
                  bg="#89b4fa", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.calculate).pack(fill="x", pady=20, ipady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="",
                                      font=("Helvetica", 16, "bold"),
                                      bg="#1e1e2e", fg="#cdd6f4")
        self.result_label.pack()

        self.category_label = tk.Label(self.root, text="",
                                        font=("Helvetica", 13),
                                        bg="#1e1e2e", fg="#cdd6f4")
        self.category_label.pack(pady=5)

        # Buttons Row
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="📊 Show Graph",
                  font=("Helvetica", 11),
                  bg="#a6e3a1", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.show_graph).pack(side="left", padx=10, ipadx=10, ipady=6)

        tk.Button(btn_frame, text="📋 View Records",
                  font=("Helvetica", 11),
                  bg="#f38ba8", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.view_records).pack(side="left", padx=10, ipadx=10, ipady=6)

        tk.Button(btn_frame, text="🔄 Reset",
                  font=("Helvetica", 11),
                  bg="#fab387", fg="#1e1e2e",
                  relief="flat", cursor="hand2",
                  command=self.reset).pack(side="left", padx=10, ipadx=10, ipady=6)

    # ─── ACTIONS ──────────────────────────────────────────────
    def calculate(self):
        name = self.name_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        try:
            weight = float(weight_str)
            height = float(height_str)
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid positive numbers for weight and height.")
            return

        bmi = calculate_bmi(weight, height)
        category, color = get_category(bmi)

        self.result_label.config(text=f"BMI: {bmi}", fg=color)
        self.category_label.config(text=f"Category: {category}", fg=color)

        save_record(name, weight, height, bmi, category)
        messagebox.showinfo("Saved", f"Record saved for {name}!")

    def show_graph(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter your name first to see your history.")
            return
        records = get_records(name)
        if len(records) < 1:
            messagebox.showinfo("No Data", f"No records found for '{name}'.")
            return

        dates = [r[0] for r in records]
        bmis  = [r[1] for r in records]

        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor("#1e1e2e")
        ax.set_facecolor("#313244")
        ax.plot(dates, bmis, marker="o", color="#89b4fa", linewidth=2)
        ax.axhline(18.5, color="#3498db", linestyle="--", alpha=0.7, label="Underweight")
        ax.axhline(25,   color="#2ecc71", linestyle="--", alpha=0.7, label="Normal")
        ax.axhline(30,   color="#f39c12", linestyle="--", alpha=0.7, label="Overweight")
        ax.set_title(f"BMI History — {name}", color="#cdd6f4")
        ax.set_xlabel("Date", color="#a6adc8")
        ax.set_ylabel("BMI", color="#a6adc8")
        ax.tick_params(colors="#a6adc8")
        ax.legend()
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def view_records(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter your name first.")
            return
        records = get_records(name)
        if not records:
            messagebox.showinfo("No Records", f"No records found for '{name}'.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Records — {name}")
        win.configure(bg="#1e1e2e")
        win.geometry("450x300")

        tk.Label(win, text=f"Records for {name}",
                 font=("Helvetica", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=10)

        cols = ("Date", "BMI", "Category")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=140)
        for r in records:
            tree.insert("", "end", values=r)
        tree.pack(padx=20, pady=10, fill="both", expand=True)

    def reset(self):
        self.name_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.category_label.config(text="")

# ─── RUN ──────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()