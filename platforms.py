import tkinter as tk
from PIL import Image, ImageTk

blocks: list[int] = []
def setup(m: tk.Tk, c: tk.Canvas):
    global master, canvas, img
    master = m
    canvas = c
    img = ImageTk.PhotoImage(
            Image.open('assets/platforms.png').crop((0,0,16,9)).resize((16*4,9*4),Image.Resampling.NEAREST)
            )
def collission_bottom(obj_id: int, to_y: float) -> bool:
    coords = list(canvas.bbox(obj_id))
    coords[1]+=to_y+12 #type: ignore
    coords[3] = coords[1] #type: ignore
    collides = list(canvas.find_overlapping(*coords))
    if obj_id in collides: collides.remove(obj_id)
    return len([block for block in blocks if block in collides]) != 0
def collision_top(obj_id: int, to_y: float) -> bool:
    coords = list(canvas.bbox(obj_id))
    coords[1] = coords[3] #type: ignore
    coords[3] += to_y #type: ignore
    collides = list(canvas.find_overlapping(*coords))
    if obj_id in collides: collides.remove(obj_id)
    return len([block for block in blocks if block in collides]) != 0
def collision_side(obj_id: int,to_x: float, offset: float) -> bool:
    coords = list(canvas.bbox(obj_id))
    coords[0]+=to_x #type: ignore
    coords[2]+=to_x #type: ignore
    coords[1]+=offset #type: ignore #knight's red thingy idk offset
    collides = list(canvas.find_overlapping(*coords))
    if obj_id in collides: collides.remove(obj_id)
    return len([block for block in blocks if block in collides]) != 0
def create_block(x: float, y: float):
    block = canvas.create_image(x,y,image=img)
    blocks.append(block)
