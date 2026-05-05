import tkinter as tk
from PIL import Image, ImageTk
import time
import ghost
import ladder
import slime
from utils import *
import platforms
knight_states = []
keys_pressed = set()
inertia = 0
gravity = 0.1
last_direction = ''
x_pos = 0
y_pos = 0
def setup_player(m: tk.Tk, c: tk.Canvas, x: float, y: float) -> int:
    global master, canvas, knight, x_pos, y_pos
    master = m
    canvas = c
    img = Image.open('assets/knight.png').convert('RGBA')
    knight_states.append([
        ImageTk.PhotoImage(img.crop((9,9,9+13,9+19)).resize((13*4,19*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((73,10,73+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((105,10,105+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((9,9,9+13,9+19)).resize((13*4,19*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((73,10,73+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((105,10,105+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT))
        ])
    knight_states.append([
        #if we recompute instead we get blinking frames, my guess is python's garbage collector
        #because tkinter holds references
        ImageTk.PhotoImage(img.crop((8,74,8+14,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((41,74,41+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((201,74,201+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((8,74,8+14,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((41,74,41+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((201,74,201+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ])
    knight = canvas.create_image(x,y,image=knight_states[0][0],anchor='nw')
    x_pos, y_pos = canvas.coords(knight)
    master.bind('<KeyPress>',on_key_press)
    master.bind('<KeyRelease>',on_key_release)
    return knight

def clock():
    global inertia,gravity,x_pos,y_pos
    # change sprite every half a second
    ts = int(time.time()*10)
    move_index = ts%3
    is_in_ladder = ladder.collides_with_ladder(knight)
    if platforms.collision_top(knight,gravity): 
        gravity = 0
    if 'a' in keys_pressed:
        inertia-=0.3
        canvas.itemconfigure(knight,image=knight_states[1][move_index+3])
    if 'd' in keys_pressed:
        inertia+=0.3
        canvas.itemconfigure(knight,image=knight_states[1][move_index])
    if 'w' in keys_pressed and is_in_ladder:
        gravity = -1
    if 's' in keys_pressed and is_in_ladder:
        gravity = 1
    if 'space' in keys_pressed and can_jump(x_pos,y_pos,knight):
        gravity = -9
    if not 'a' in keys_pressed and not 'd' in keys_pressed:
        if last_direction == 'd':
            canvas.itemconfigure(knight,image=knight_states[0][move_index])
        else:
            canvas.itemconfigure(knight,image=knight_states[0][move_index+3])
    if platforms.collision_side(knight,inertia,12):
        inertia = 0
    if platforms.collission_bottom(knight,gravity):
        gravity = 0
    inertia = round(inertia,2)
    y_pos = min(y_pos+gravity,720-19*6)
    x_pos = clamp(x_pos+inertia,0,980-13*4)
    canvas.coords(knight,x_pos,y_pos)
    if inertia > 0: inertia-=0.1
    elif inertia < 0: inertia+=0.1
    if is_in_ladder and ('w' in keys_pressed or 's' in keys_pressed): gravity = 0
    else: gravity+=0.4
    inertia = clamp(inertia,-5,5) #speed cap
    gravity = min(gravity,15) #terminal velocity
    if collides_with_enemy():
        kill()
    master.after(16,clock)

def on_key_press(e: tk.Event[tk.Misc]):
    global last_direction
    key = e.keysym
    if key in ('a','d'): last_direction = key
    keys_pressed.add(key)
def on_key_release(e: tk.Event[tk.Misc]):
    key = e.keysym
    if key in keys_pressed:
        keys_pressed.remove(key)

def collides_with_enemy() -> bool:
    bbox = canvas.bbox(knight)
    collissions = canvas.find_overlapping(*bbox)
    return len([x for x in slime.slimes+ghost.ghosts if x[0] in collissions]) != 0

def kill():
    print('ded')
