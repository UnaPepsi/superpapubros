import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import player, slime, ghost, platforms, ladder
from PIL import Image, ImageTk
import sys
import re

editor_open = False
index_selected = None
level_dat: list[tuple[int,...]]
buttons: list[tk.Button]

def setup_editor(m: tk.Tk, bg: ImageTk.PhotoImage):
    global master, canvas, editor_open, level_dat, buttons_img, buttons
    if editor_open: return
    editor_open = True
    level_dat = []
    buttons_img = []
    buttons = []
    master = tk.Toplevel(m)
    master.protocol("WM_DELETE_WINDOW", lambda : on_close())
    master.geometry('980x720')
    master.resizable(False,False)
    canvas = tk.Canvas(master)
    canvas.pack(fill='both',expand=True)
    canvas.create_image(0,0,image=bg,anchor='nw')
    buttons_img.append(
        ImageTk.PhotoImage(player.img.crop((9,9,9+13,9+19)).resize((13*4,19*4),Image.Resampling.NEAREST)),
            )
    buttons.append(tk.Button(canvas,image=buttons_img[0],command=lambda : change_index(0)))
    buttons_img.append(
            ImageTk.PhotoImage(slime.img.crop((5,15,5+14,15+9)).resize((14*4,9*4),Image.Resampling.NEAREST)),
                       )
    buttons.append(tk.Button(canvas,image=buttons_img[1],command=lambda : change_index(1)))
    buttons_img.append(
            ImageTk.PhotoImage(ghost.img.crop((5,5,5+21,5+25)).resize((21*3,25*3),Image.Resampling.NEAREST)),
                        )
    buttons.append(tk.Button(canvas,image=buttons_img[2],command=lambda : change_index(2)))
    buttons_img.append(platforms.img)
    buttons.append(tk.Button(canvas,image=buttons_img[3],command=lambda : change_index(3)))
    buttons_img.append(ladder.img)
    buttons.append(tk.Button(canvas,image=buttons_img[4],command=lambda : change_index(4)))
    buttons.append(tk.Button(canvas,text='Meta',height=2,command=lambda : change_index(-1)))
    buttons.append(tk.Button(canvas,text='Guardar',height=2,command=save_level))
    for i,btn in enumerate(buttons):
        btn.place(x=i*81,y=0,width=80,height=80)
    canvas.delete('all')
    canvas.bg_tag = canvas.create_image(0,0,image=bg,anchor='nw') #type: ignore
    canvas.bind('<Button-1>',place)
    #"For odd historical reasons, the right button is button 2 on the Mac, but 3 on unix and windows."
    #https://stackoverflow.com/questions/30668425/tkinter-right-click-popup-unresponsive-on-osx#:~:text=For%20odd%20historical%20reasons%2C%20the%20right%20button%20is%20button%202%20on%20the%20Mac%2C%20but%203%20on%20unix%20and%20windows.
    if sys.platform.lower() == 'darwin':
        canvas.bind('<Button-2>',remove)
    else:
        canvas.bind('<Button-3>',remove)

def change_index(i: int):
    global index_selected
    index_selected = i

def snap(x: int, y: int) -> tuple[int,int]:
    tile_x = 64 #height of platforms
    tile_y = 36 #height of platforms
    grid_x = round(x / tile_x) * tile_x
    grid_y = round(y / tile_y) * tile_y
    return grid_x,grid_y

def place(event: tk.Event[tk.Canvas]):
    if index_selected is None: return
    x,y = snap(event.x,event.y)
    for dat in level_dat:
        #if player already in level
        if dat[2] == 0 == index_selected: return
        #if the same item is placed twice
        if dat[0]==x and dat[1]==y and dat[2] == index_selected: return
    print('placing',x,y)
    if index_selected == -1: obj_id = canvas.create_rectangle(x,y,x,y,fill='red',width=20)
    else: obj_id = canvas.create_image(x,y,image=buttons_img[index_selected])
    level_dat.append((x,y,index_selected,obj_id))

def remove(event: tk.Event[tk.Canvas]):
    global level_dat
    x,y = event.x,event.y
    collisions = canvas.find_overlapping(x,y,x,y)
    for collision in collisions:
        if collision == canvas.bg_tag: continue #type: ignore
        canvas.delete(collision)
        level_dat = list(filter(lambda x: x[-1]!=collision,level_dat))

def save_level():
    name = askstring(title='Guardado',prompt='Escribe el nombre del nivel (solo caracteres alfanuméricos y guiones')
    if not name: return
    if re.match(r'(?![\w|-])',name):
        messagebox.showerror(message='Solo caracteres alfanuméricos y guiones')
        return
    with open('levels/'+name+'.dat','w') as f:
        for dat in level_dat:
            f.write(f'{dat[0]}|{dat[1]}|{dat[2]}\n')
    messagebox.showinfo(message='Guardado con éxito :)')

def on_close():
    global editor_open
    master.destroy()
    editor_open = False
