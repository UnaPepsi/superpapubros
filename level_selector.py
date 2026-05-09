from tkinter import Canvas, Event, Listbox, Tk, Toplevel, Label, BooleanVar
from os import listdir
from tkinter.font import Font
import ghost
import ladder
import platforms
import player
import slime

current_level = ''
callbacks = []

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
    global current_level
    select = e.widget.curselection()
    if not select: return
    select = int(select[0])
    current_level = 'levels/'+e.widget.get(select)
    create_level()

def create_level():
    canvas.delete('all')
    canvas.create_image(0,0,image=canvas.bg_tk,anchor='nw') #type: ignore
    with open(current_level,'r') as f:
        lines = list(map(lambda x: x.removesuffix('\n').split('|'),f.readlines()))
        p = next(filter(lambda x: x[-1]=='0',lines))
        p = list(map(int, p))
        p_id = player.setup_player(master,canvas,p[0],p[1])
        slime.setup_slime(master,canvas,p_id)
        ghost.setup_ghost(master,canvas,p_id)
        for line in lines:
            line = list(map(int, line))
            if line[-1] == 1:
                slime.create_slime(line[0],line[1])
            elif line[-1] == 2:
                ghost.create_ghost(line[0],line[1])
            elif line[-1] == 3:
                platforms.create_block(line[0],line[1])
            elif line[-1] == 4:
                ladder.place_ladder(line[0],line[1])
            elif line[-1] == -1:
                player.add_goal(line[0],line[1])
        tl.destroy()
        a = BooleanVar(canvas,True)
        countdown(3,a,None)
        canvas.wait_variable(a)
        callbacks.append(player.clock())
        callbacks.append(slime.clock())
        callbacks.append(ghost.clock())

def countdown(t: int,var: BooleanVar,tid: int | None = None):
    if tid is not None:
        canvas.delete(tid)
    if t <= 0:
        return var.set(False)
    f=Font(canvas,size=50)
    tid = canvas.create_text(980/2,720/2,anchor='center',text=t,font=f)
    canvas.after(333,lambda : countdown(t-1,var,tid))
