import time
from PIL import Image, ImageTk
import tkinter as tk
import platforms

img = Image.open('assets/slime_green.png')

def setup_slime(m: tk.Tk, c: tk.Canvas, knight_id: int):
    global master, canvas, idling, aggro, knight, slimes, slimes_aggro
    master = m
    canvas = c
    knight = knight_id
    slimes = []
    slimes_aggro = []
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
    aggro_speed = 3
    coords = canvas.coords(knight)
    if not coords: return
    kx,ky = coords
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
        coll_side = platforms.collision_side(slime,slimes[i][1],-1,-15)
        #other offset to add slime's velocity. without this slime may move to illegal spot then get stuck
        coll_top = platforms.collision_top(slime,15,slimes[i][1]*(25 if abs(slimes[i][1]) == 2 else 5))
        #last or just borders
        if coll_side or (not coll_top and y < 720-20) \
                or x+slimes[i][1] <= 0 or x+slimes[i][1] >= 980:
            slimes[i][1] *= -1
        #if slime spawns on the air, let it fall until it hits a platform
        coll_top = platforms.collision_top(slime,15,slimes[i][1])
        if coll_top:
            canvas.coords(slime,x,coll_top-0.5)
        gravity = 2 if y < 720-20 else 0
        canvas.move(slime,slimes[i][1],gravity)
    return master.after(16,clock)

def create_slime(x: float, y: float):
    slime = canvas.create_image(x,y,image=idling[0])
    base_speed = 2
    slimes.append([slime,base_speed])
