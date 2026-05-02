import tkinter as tk
import time
import threading
from PIL import Image, ImageTk
from utils import can_jump, clamp
master = tk.Tk()
master.geometry('980x720')
BORDERS = 980,720
knight_states = {}
keys_pressed = set()

img = Image.open('assets/knight.png')
knight_states['idle'] = [
        ImageTk.PhotoImage(img.crop((9,9,9+13,9+19)).resize((13*4,19*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((73,10,73+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((105,10,105+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((9,9,9+13,9+19)).resize((13*4,19*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((73,10,73+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((105,10,105+13,10+18)).resize((13*4,19*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT))
        ]
knight_states['move'] = [
        #if we recompute instead we get blinking frames, my guess is python's garbage collector
        #because tkinter holds references
        ImageTk.PhotoImage(img.crop((8,74,8+14,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((41,74,41+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((201,74,201+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST)),
        ImageTk.PhotoImage(img.crop((8,74,8+14,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((41,74,41+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ImageTk.PhotoImage(img.crop((201,74,201+13,74+18)).resize((14*4,18*4),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
        ]
knight = tk.Label(master,image=knight_states['idle'][0])
knight.pack()
inertia = 0
gravity = 0.1
last_direction = ''

def clock():
    global inertia,gravity
    # change sprite every half a second
    ts = int(time.time()*10)
    move_index = ts%3
    if 'a' in keys_pressed:
        inertia-=0.3
        knight.configure(image=knight_states['move'][move_index+3])
    elif 'd' in keys_pressed:
        inertia+=0.3
        knight.configure(image=knight_states['move'][move_index])
    if 'space' in keys_pressed and can_jump(knight.winfo_x(),knight.winfo_y()):
        gravity = -9
    else:
        if last_direction == 'd':
            knight.configure(image=knight_states['idle'][move_index])
        else:
            knight.configure(image=knight_states['idle'][move_index+3])
    knight.place_configure(x=clamp(knight.winfo_x()+inertia,0,BORDERS[0]-13*4),
                           y=min(knight.winfo_y()+gravity,720-19*6))
    # time.sleep(1/60)
    if inertia > 0: inertia-=0.1
    elif inertia < 0: inertia+=0.1
    if knight.winfo_y() < 720:
        gravity+=0.4
    inertia = clamp(inertia,-5,5) #speed cap
    gravity = min(gravity,15) #terminal velocity
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
        # knight.configure(image=knight_states['idle'])

# threading.Thread(target=clock,daemon=True).start()

master.bind('<KeyPress>',on_key_press)
master.bind('<KeyRelease>',on_key_release)
clock()
master.mainloop()
