import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from win10toast import ToastNotifier
from multiprocessing import Process
import time
import random
import screeninfo
import os

def show_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5, threaded=True)
    while toaster.notification_active():
        time.sleep(0.1)

def run_gif_popup(gif_path, duration=10000, width=300, height=300):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    screen = screeninfo.get_monitors()[0]
    x = random.randint(0, screen.width - width)
    y = random.randint(0, screen.height - height)
    root.geometry(f"{width}x{height}+{x}+{y}")

    label = tk.Label(root)
    label.pack()

    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

    def update(index):
        label.configure(image=frames[index])
        root.after(100, update, (index + 1) % len(frames))

    update(0)
    root.after(duration, root.destroy)
    root.mainloop()


def show_multiple_gif_popups(gif_path, count=5, delay_between=300):
    processes = []
    for _ in range(count):
        p = Process(target=run_gif_popup, args=(gif_path,))
        p.start()
        processes.append(p)
        time.sleep(delay_between / 1000.0) 

# === MAIN ===
if __name__ == "__main__":
    gif_path = r"soy-point.gif" 

    if not os.path.exists(gif_path):
        print("❌ GIF file not found:", gif_path)
    else:
        show_notification("Karma...", "Incoming!\n\n")
        show_multiple_gif_popups(gif_path, count=50, delay_between=100) 
