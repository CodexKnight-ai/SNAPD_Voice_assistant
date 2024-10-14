import tkinter as tk
from PIL import Image, ImageTk
import pygame
import subprocess
import sys


class SNAPD(tk.Frame):
    def __init__(self, root):
        super().__init__(
            root,
            bg='BLACK'
        )
        self._root = root  # Store root reference in _root
        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.label_gif1 = tk.Label(
            self.main_frame,                    
            bg='BLACK',
            border=0,
            highlightthickness=0    #247 frames
        )
        self.label_gif1.grid(column=0, row=0)

        self.gif1_frames = self._get_frames('final_intro.gif')

        pygame.init()
        pygame.mixer.music.load("final.mp3")

        # Play the music and start the GIF animation
        pygame.mixer.music.play()
        self._play_gif()

    def _get_frames(self, img):
        with Image.open(img) as gif:
            index = 0
            frames = []
            while True:
                try:
                    gif.seek(index)
                    frame = ImageTk.PhotoImage(gif)
                    frames.append(frame)
                except EOFError:
                    break

                index += 1

            return frames

    def _play_gif(self):
        total_delay = 50
        delay_frames = 44
        for frame in self.gif1_frames:
            self._root.after(total_delay, self._next_frame, frame)
            total_delay += delay_frames

        # Stop the music when the GIF ends
        self._root.after(total_delay, self._on_finished)

    def _next_frame(self, frame):
        self.label_gif1.config(
            image=frame
        )

    def _on_finished(self):
        pygame.mixer.music.stop()
        self._root.destroy()  # Close the window 
        subprocess.Popen(["python", "SNAPD VA.py"])  # Name of your main program

for i in range(3):
    a = input("Enter Password to open SNAPD :- ")
    with open('A:/CodexKnight training/Python/ai/password.txt', 'r') as pw_file:
        pw = pw_file.read()
    if (a==pw):
        print("WELCOME BOSS!")
        root = tk.Tk()
        root.title("SNAPD")
        root.geometry('1535x833')
        root.resizable(width=False, height=False)
        SNAPD_instance = SNAPD(root)
        root.mainloop()
        break
    elif (i==2 and a!=pw):
        print("Unknown Entry")
        sys.exit()
    else:
        print("Try Again")
