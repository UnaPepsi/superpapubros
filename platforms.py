import tkinter as tk
from PIL import Image, ImageTk

blocks: list[tk.Label] = []
def setup(m: tk.Tk):
    global master, img
    master = m
    img = ImageTk.PhotoImage(
            Image.open('assets/platforms.png').crop((0,0,16,9)).resize((16*4,9*4),Image.Resampling.NEAREST)
            )
def collision_top(future_x: float, future_y: float) -> tuple[bool,float]:
    tolerance = 4
    future_y +=19*4
    for block in blocks:
        x,y = block.winfo_x(),block.winfo_y()
        if x-13*4 < future_x < x+16*4 and future_y <= y and future_y >= y-tolerance:
            return True,y
    return False,-1
def collision_size(future_x: float, future_y: float) -> float:
    tolerance = 3
    for block in blocks:
        x,y = block.winfo_x(),block.winfo_y()
        y+=9*4
        if x-13*4 < future_x < x+16*4 and future_y >= y and future_y <= y-tolerance:
            # print('yes',x,future_x)
            return True
    return False
def create_block(x: float, y: float):
    block = tk.Label(master,image=img)
    block.place(x=x,y=y)
    blocks.append(block)
