import os
import time

from dotenv import load_dotenv
import tkinter as tk
from PIL import Image, ImageTk
import requests
from datetime import datetime
import threading

load_dotenv()
api_key = os.getenv('API_KEY')


class SlideShowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Painel Slides")
        self.geometry("800x600")
        self.attributes("-fullscreen", True)

        self.slides = ["img-1.jpg", "img-2.jpg", "img-3.jpg"]
        self.current_slide = 0

        self.slide_label = tk.Label(self)
        self.slide_label.pack(expand=True, fill=tk.BOTH)

        self.info_bar = tk.Frame(self, height=100, bg='#282828')
        self.info_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.time_label = tk.Label(self.info_bar, text="", bg='#282828', fg='white', font=("Helvetica", 12))
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=10)

        self.dollar_label = tk.Label(self.info_bar, text="", bg='#282828', fg='white', font=("Helvetica", 12))
        self.dollar_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.news_canvas = tk.Canvas(self.info_bar, bg='#282828', height=30, highlightthickness=0)
        self.news_canvas.pack(fill=tk.X, padx=30, pady=10)
        self.news_canvas_text = self.news_canvas.create_text(0, 15, text="", anchor="w", fill="white",
                                                             font=("Helvetica", 12))

        self.news_items = []
        self.news_index = 0

        self.update_time()
        threading.Thread(target=self.update_dollar_rate).start()
        threading.Thread(target=self.update_news).start()
        self.show_slide()
        self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))
        self.bind('<F11>', lambda e: self.attributes('-fullscreen', True))

    def show_slide(self):
        img = Image.open(self.slides[self.current_slide])
        img = img.resize((800, 500), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(img)
        self.slide_label.config(image=self.img)
        self.current_slide = (self.current_slide + 1) % len(self.slides)
        self.after(10000, self.show_slide)

    def update_time(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    def update_news(self):
        try:
            response = requests.get(f'https://newsapi.org/v2/top-headlines?country=br&apiKey={api_key}')
            data = response.json()
            self.news_items = [article["title"] for article in data["articles"]]
            self.news_index = 0
            self.scroll_news()
        except Exception as e:
            self.news_canvas.itemconfig(self.news_canvas_text, text="Falha ao carregar notícias")
        time.sleep(160)

    def scroll_news(self):
        if self.news_items:
            current_text = "  /  ".join(self.news_items)
            self.news_canvas.itemconfig(self.news_canvas_text, text=current_text)
            bbox = self.news_canvas.bbox(self.news_canvas_text)
            if bbox[2] < 0:
                self.news_index = (self.news_index + 1) % len(self.news_items)
                self.news_canvas.coords(self.news_canvas_text, 800, 15)
            else:
                self.news_canvas.move(self.news_canvas_text, -2, 0)
            self.news_canvas.after(50, self.scroll_news)

    def update_dollar_rate(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            brl_rate = data["rates"]["BRL"]
            self.dollar_label.config(text=f"USD to BRL: R${brl_rate:.2f}")
        except Exception as e:
            self.dollar_label.config(text="Falha ao obter informações sobre o dólar.")
        time.sleep(3600)


if __name__ == "__main__":
    app = SlideShowApp()
    app.mainloop()
