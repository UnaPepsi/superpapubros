from PIL import Image, ImageTk
import tkinter as tk

ladders = []

def setup_ladder(m: tk.Tk, c: tk.Canvas):
    global master, canvas, img
    master = m
    canvas = c
    img = ImageTk.PhotoImage(
            Image.open('assets/Ladder_1.png').crop((3,2,3+12,2+30)).resize((12*4,30*4),Image.Resampling.NEAREST)
            )

def place_ladder(x: float, y: float):
    ladder = canvas.create_image(x,y,image=img)
    ladders.append(ladder)

def collides_with_ladder(obj_id: int) -> bool:
    bbox = canvas.bbox(obj_id)
    collissions = canvas.find_overlapping(*bbox)
    return any(x for x in ladders if x in collissions)
