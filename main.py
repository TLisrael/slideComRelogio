import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from datetime import datetime
import threading
import time


class SlideShowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wood PLC Info")
        self.geometry("800x600")

        self.slides = ["WOOD-PLC-.jpg", "wood.jpg", "WOOD-PLC-.jpg", "wood.jpg", "WOOD-PLC-.jpg", "wood.jpg",
                       "WOOD-PLC-.jpg", "wood.jpg"]
        self.current_slide = 0

        self.slide_label = tk.Label(self)
        self.slide_label.pack(expand=True, fill=tk.BOTH)

        self.info_bar = tk.Frame(self, height=100, bg='#282828')
        self.info_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.time_label = tk.Label(self.info_bar, text="", bg='#282828', fg='white', font=("Helvetica", 16))
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=10)

        self.dollar_label = tk.Label(self.info_bar, text="", bg='#282828', fg='white', font=("Helvetica", 16))
        self.dollar_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.news_canvas = tk.Canvas(self.info_bar, bg='#282828', height=30, highlightthickness=0)
        self.news_canvas.pack(fill=tk.X, padx=20)
        self.news_canvas_text = self.news_canvas.create_text(0, 15, text="", anchor="w", fill="white",
                                                             font=("Helvetica", 16))

        self.show_slide()

    def show_slide(self):
        img = Image.open(self.slides[self.current_slide])
        img = img.resize((800, 500), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(img)
        self.slide_label.config(image=self.img)
        self.current_slide = (self.current_slide + 1) % len(self.slides)
        self.after(10000, self.show_slide)

    def update_time(self):
        now = datetime.now().strftime("%d/%m-%Y %H:%M")
        self.time_label.config(text=now)
        self.after(1000, self.update_time)


if __name__ == "__main__":
    app = SlideShowApp()
    app.mainloop()
