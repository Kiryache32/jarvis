import tkinter as tk
from app.planner import planner

class JarvisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis Online")

        self.output = tk.Text(self.root, height=15)
        self.output.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x")

        self.btn = tk.Button(self.root, text="Отправить", command=self.send)
        self.btn.pack(fill="x")

    def log(self, text):
        self.output.insert("end", text + "\n")
        self.output.see("end")

    def send(self):
        user_text = self.entry.get()
        self.entry.delete(0, "end")

        self.log(f"> {user_text}")

        response = planner(user_text)
        self.log(response)

    def run(self):
        self.root.mainloop()
