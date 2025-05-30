import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
import os
import re

file_map = {
    "Substance": "substance.txt",
    "Digital": "digital.txt",
    "Food": "food.txt",
    "Gambling": "gambling.txt"
}

class ChallengeApp:
    def __init__(self, root):
        self.root = root
        root.title("21-Days Challenges")
        root.geometry("600x450")

        # Initialize pyttsx3 engine once here for speed
        self.engine = pyttsx3.init()

        # Dropdown menu
        tk.Label(root, text="Choose an addiction type:").pack(pady=5)
        self.selected = tk.StringVar(value="Substance")
        self.drop = tk.OptionMenu(root, self.selected, *file_map.keys())
        self.drop.pack(pady=5)

        # Load button
        self.load_btn = tk.Button(root, text="Load Challenge", command=self.load_challenge)
        self.load_btn.pack(pady=5)

        # Text box
        self.text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
        self.text_box.pack(padx=10, pady=10)

        # Navigation buttons frame
        nav_frame = tk.Frame(root)
        nav_frame.pack(pady=10)

        self.prev_btn = tk.Button(nav_frame, text="Previous Day", command=self.prev_day, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=10)

        self.speak_btn = tk.Button(nav_frame, text="Speak Day", command=self.speak_day, state=tk.DISABLED)
        self.speak_btn.pack(side=tk.LEFT, padx=10)

        self.next_btn = tk.Button(nav_frame, text="Next Day", command=self.next_day, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=10)

        # Variables to track challenge
        self.days = []
        self.current_day = 0

    def load_challenge(self):
        addiction = self.selected.get()
        filename = file_map.get(addiction)
        if not filename or not os.path.exists(filename):
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, "Challenge file not found.")
            self.disable_nav_buttons()
            return
        
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        # Split content into days using regex pattern "Day X:" (case-insensitive)
        pattern = re.compile(r"(Day \d+:.*?)(?=Day \d+:|$)", re.DOTALL | re.IGNORECASE)
        self.days = pattern.findall(content)

        if not self.days:
            # fallback to whole content if no days found
            self.days = [content]

        # Add special message to day 21 if exists
        if len(self.days) >= 21:
            congrats_msg = "\n\n🎉 Congratulations! You made it to Day 21! Wishing you a happy life ahead! 🎉"
            self.days[20] = self.days[20].strip() + congrats_msg

        self.current_day = 0
        self.show_day()
        self.update_nav_buttons()

    def show_day(self):
        self.text_box.delete("1.0", tk.END)
        day_text = self.days[self.current_day].strip()
        day_header = f"--- {self.selected.get()} Challenge: Day {self.current_day + 1} / {len(self.days)} ---\n\n"
        self.text_box.insert(tk.END, day_header + day_text)

    def speak_day(self):
        day_text = self.days[self.current_day].strip()
        self.engine.say(day_text)
        self.engine.runAndWait()

    def prev_day(self):
        if self.current_day > 0:
            self.current_day -= 1
            self.show_day()
            self.update_nav_buttons()

    def next_day(self):
        if self.current_day < len(self.days) - 1:
            self.current_day += 1
            self.show_day()
            self.update_nav_buttons()

    def update_nav_buttons(self):
        self.prev_btn.config(state=tk.NORMAL if self.current_day > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_day < len(self.days) - 1 else tk.DISABLED)
        self.speak_btn.config(state=tk.NORMAL if self.days else tk.DISABLED)

    def disable_nav_buttons(self):
        self.prev_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        self.speak_btn.config(state=tk.DISABLED)


root = tk.Tk()
app = ChallengeApp(root)
root.mainloop()
