from tkinter import Canvas, Event, Listbox, Tk, Toplevel, Label
from os import listdir

import ghost
import platforms
import player
import slime
def show_levels(m: Tk,c: Canvas):
    global master, canvas, tl
    master = m
    canvas = c
    tl = Toplevel(m)
    tl.title('Niveles')
    tl.resizable(False,False)
    Label(tl,text='Selecciona un nivel').pack()
    lsbox = Listbox(tl)
    lsbox_i = 0
    for path in listdir('levels'):
        if path.endswith('.dat'):
            lsbox.insert(lsbox_i,path.removesuffix('levels/'))
        lsbox_i+=1
    height = max(400,10*lsbox_i)
    lsbox.configure(height=height)
    tl.geometry('200x'+str(height))
    lsbox.pack()
    lsbox.bind('<<ListboxSelect>>',on_select_level)

def on_select_level(e: Event[Listbox]):
    select = e.widget.curselection()
    if not select: return
    select = int(select[0])
    lvl = 'levels/'+e.widget.get(select)
    create_level(lvl)

def create_level(path: str):
    canvas.delete('all')
    canvas.create_image(0,0,image=canvas.bg_tk,anchor='nw') #type: ignore
    with open(path,'r') as f:
        lines = list(map(lambda x: x.removesuffix('\n').split('|'),f.readlines()))
        p = next(filter(lambda x: x[-1]=='0',lines))
        p = list(map(int, p))
        p_id = player.setup_player(master,canvas,p[0],p[1])
        slime.setup_slime(master,canvas,p_id)
        ghost.setup_ghost(master,canvas,p_id)
        platforms.setup(master,canvas)
        for line in lines:
            line = list(map(int, line))
            if line[-1] == 1:
                slime.create_slime(line[0],line[1])
            elif line[-1] == 2:
                ghost.create_ghost(line[0],line[1])
            elif line[-1] == 3:
                platforms.create_block(line[0],line[1])
            elif line[-1] == -1:
                player.add_goal(line[0],line[1])
        player.clock()
        slime.clock()
        ghost.clock()
    tl.destroy()
