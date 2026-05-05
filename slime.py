import time
from PIL import Image, ImageTk
import tkinter as tk
import platforms

slimes = []
slimes_aggro = []

def setup_slime(m: tk.Tk, c: tk.Canvas, knight_id: int):
    global master, canvas, idling, aggro, knight
    master = m
    canvas = c
    knight = knight_id
    img = Image.open('assets/slime_green.png')
    idling = [
            ImageTk.PhotoImage(img.crop((5,15,5+14,15+9)).resize((14*4,9*4),Image.Resampling.NEAREST)),
            ImageTk.PhotoImage(img.crop((29,14,29+14,14+10)).resize((14*4,10*4),Image.Resampling.NEAREST)),
            ]
    aggro = [
            ImageTk.PhotoImage(img.crop((53,13,53+14,13+11)).resize((14*4,11*4),Image.Resampling.NEAREST)),
            ImageTk.PhotoImage(img.crop((5,36,5+14,36+12)).resize((14*4,12*4),Image.Resampling.NEAREST)),
            ImageTk.PhotoImage(img.crop((29,35,29+14,35+13)).resize((14*4,13*4),Image.Resampling.NEAREST)),
            ImageTk.PhotoImage(img.crop((53,33,53+14,33+15)).resize((14*4,15*4),Image.Resampling.NEAREST)),
            ]

def _make_slime_aggro(slime: int, index: int):
    if slime not in slimes_aggro:
        return
    if index == 4:
        index = 2
    canvas.itemconfigure(slime,image=aggro[index])
    master.after(125,_make_slime_aggro,slime,index+1)

def clock():
    aggro_speed = 5
    kx,ky = canvas.coords(knight)
    ts = int(time.time())
    idle_index = ts%2
    for i,e in enumerate(slimes):
        slime = e[0]
        x,y = canvas.coords(slime)
        # if math.sqrt((kx-x)**2 + (ky-y)**2) < 300:
        if (kx-x)**2 + (ky-y)**2 < 90_000: #a lil bit faster
            if slime not in slimes_aggro:
                slimes_aggro.append(slime)
                slimes[i][1] *= aggro_speed
                master.after(0,_make_slime_aggro,slime,0)
        else:
            if slime in slimes_aggro:
                slimes[i][1] /= aggro_speed
                slimes_aggro.remove(slime)
            canvas.itemconfigure(slime,image=idling[idle_index])
        #offset cuz slime grows when agro
        #other offset to add slime's velocity. without this slime may move to illegal spot then get stuck
        #last or just borders
        if platforms.collision_side(slime,slimes[i][1],-1,-15) \
                or (not platforms.collision_top(slime,15,slimes[i][1]) and y < 720-15*4) \
                or x+slimes[i][1] <= 0 or x+slimes[i][1] >= 980:
            slimes[i][1] *= -1
        canvas.move(slime,slimes[i][1],0)
    master.after(16,clock)

def create_slime(x: float, y: float):
    slime = canvas.create_image(x,y,image=idling[0])
    base_speed = 2
    slimes.append([slime,base_speed])
