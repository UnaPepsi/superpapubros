import time
from PIL import Image, ImageTk
import tkinter as tk

ghosts = []

def setup_ghost(m: tk.Tk, c: tk.Canvas, knight_id: int):
    global master, canvas, states, knight
    master = m
    canvas = c
    img = Image.open('assets/MiniGhost_Idle.png')
    states = [
            ImageTk.PhotoImage(img.crop((5,5,5+21,5+25)).resize((21*3,25*3),Image.Resampling.NEAREST)),
            ImageTk.PhotoImage(img.crop((69,3,69+21,3+26)).resize((21*3,26*3),Image.Resampling.NEAREST)),
            ImageTk.PhotoImage(img.crop((133,3,133+22,3+22)).resize((22*3,22*3),Image.Resampling.NEAREST)),
            ]
    knight = knight_id

def clock():
    ts = int(time.time()*10)
    move_index = ts%3
    kx,ky = canvas.coords(knight)
    ky+=19*4 #point to feet
    for ghost in ghosts:
        gh = ghost[0]
        x,y = canvas.coords(gh)
        dx = kx-x
        dy = ky-y
        dist = (dx**2 + dy**2) ** 0.5
        max_speed = 2
        max_force = 0.015
        desired_vx = dx / dist * max_speed if dist != 0 else 0
        desired_vy = dy / dist * max_speed if dist != 0 else 0
        steer_x = desired_vx - ghost[1]
        steer_y = desired_vy - ghost[2]
        steer_mag = (steer_x**2 + steer_y**2) ** 0.5
        if steer_mag > max_force:
            steer_x = steer_x / steer_mag * max_force
            steer_y = steer_y / steer_mag * max_force
        ghost[1]+=steer_x
        ghost[2]+=steer_y
        canvas.move(gh,ghost[1],ghost[2])
        canvas.itemconfigure(gh,image=states[move_index])
    master.after(16,clock)

def create_ghost(x,y):
    ghost = canvas.create_image(x,y,image=states[0])
    ghosts.append([ghost,0,0])
