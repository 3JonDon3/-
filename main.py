import tkinter as tk
from tkinter import messagebox
import random

class MillionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Перший мільйон")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e2f")

        self.money_levels = [1000, 5000, 10000, 50000, 100000, 250000, 500000, 1000000]
        self.current_question = 0
        self.used_5050 = False

        self.questions = [
            {
                "question": "Столиця Франції?",
                "options": ["Берлін", "Париж", "Мадрид", "Рим"],
                "answer": 1
            },
            {
                "question": "12 × 12 = ?",
                "options": ["124", "144", "132", "154"],
                "answer": 1
            },
            {
                "question": "Найбільший океан?",
                "options": ["Атлантичний", "Індійський", "Тихий", "Північний Льодовитий"],
                "answer": 2
            },
            {
                "question": "Автор 'Гамлета'?",
                "options": ["Шекспір", "Діккенс", "Гете", "Байрон"],
                "answer": 0
            },
            {
                "question": "Хімічний символ золота?",
                "options": ["Au", "Ag", "Fe", "O"],
                "answer": 0
            },
            {
                "question": "Скільки кісток у дорослої людини?",
                "options": ["206", "210", "198", "250"],
                "answer": 0
            },
            {
                "question": "Найшвидша наземна тварина?",
                "options": ["Лев", "Гепард", "Тигр", "Антилопа"],
                "answer": 1
            },
            {
                "question": "Мова програмування Python названа на честь?",
                "options": ["Змії", "Вченого", "Комедійного шоу", "Бога"],
                "answer": 2
            }
        ]

        random.shuffle(self.questions)

        self.label_money = tk.Label(root, text="", font=("Arial", 16), fg="gold", bg="#1e1e2f")
        self.label_money.pack(pady=10)

        self.label_question = tk.Label(root, text="", font=("Arial", 14), wraplength=500, bg="#1e1e2f", fg="white")
        self.label_question.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", width=40, height=2,
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.btn_5050 = tk.Button(root, text="50/50", command=self.use_5050)
        self.btn_5050.pack(pady=10)

        self.load_question()

    def load_question(self):
        q = self.questions[self.current_question]
        self.label_money.config(text=f"Питання на {self.money_levels[self.current_question]} грн")
        self.label_question.config(text=q["question"])

        for i in range(4):
            self.buttons[i].config(text=q["options"][i], state="normal")

    def check_answer(self, choice):
        correct = self.questions[self.current_question]["answer"]

        if choice == correct:
            self.current_question += 1
            if self.current_question == len(self.questions):
                messagebox.showinfo("Перемога!", "🎉 Ти виграв ПЕРШИЙ МІЛЬЙОН!")
                self.root.quit()
            else:
                self.load_question()
        else:
            win_money = self.money_levels[self.current_question - 1] if self.current_question > 0 else 0
            messagebox.showerror("Гра завершена", f"Неправильно!\nТвій виграш: {win_money} грн")
            self.root.quit()

    def use_5050(self):
        if self.used_5050:
            return

        correct = self.questions[self.current_question]["answer"]
        wrong_indexes = [i for i in range(4) if i != correct]
        remove = random.sample(wrong_indexes, 2)

        for i in remove:
            self.buttons[i].config(state="disabled")

        self.used_5050 = True
        self.btn_5050.config(state="disabled")


root = tk.Tk()
game = MillionGame(root)
root.mainloop()