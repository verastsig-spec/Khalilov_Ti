import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

class RandomTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("400x500")

        # 1. Данные
        self.tasks_pool = [
            {"text": "Прочитать статью", "type": "Учёба"},
            {"text": "Сделать зарядку", "type": "Спорт"},
            {"text": "Разобрать почту", "type": "Работа"},
            {"text": "Выучить 5 слов", "type": "Учёба"},
            {"text": "Пробежка 15 мин", "type": "Спорт"},
            {"text": "Написать отчет", "type": "Работа"}
        ]
        self.history = []
        self.file_path = "history.json"

        self.load_history()
        self.setup_ui()

    def setup_ui(self):
        # Кнопка генерации
        self.gen_btn = tk.Button(self.root, text="🎲 Сгенерировать задачу", command=self.generate_task, bg="#4CAF50", fg="white")
        self.gen_btn.pack(pady=10, fill=tk.X, padx=20)

        # Фильтрация
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["Все", "Учёба", "Спорт", "Работа"])
        self.filter_menu.pack(side=tk.LEFT, padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.update_history_display)

        # Список истории
        tk.Label(self.root, text="История задач:").pack()
        self.history_listbox = tk.Listbox(self.root, height=15)
        self.history_listbox.pack(pady=5, fill=tk.BOTH, padx=20, expand=True)

        self.update_history_display()

    def generate_task(self):
        task = random.choice(self.tasks_pool)
        self.history.append(task)
        self.save_history()
        self.update_history_display()
        messagebox.showinfo("Новая задача", f"{task['text']} ({task['type']})")

    def update_history_display(self, event=None):
        self.history_listbox.delete(0, tk.END)
        filter_val = self.filter_var.get()
        
        for item in reversed(self.history):
            if filter_val == "Все" or item['type'] == filter_val:
                self.history_listbox.insert(tk.END, f"[{item['type']}] {item['text']}")

    def save_history(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.history = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskApp(root)
    root.mainloop()
