import tkinter as tk
from level_selector import show_levels
import editor, platforms, ladder
from PIL import ImageTk, Image

master = tk.Tk()
master.geometry('980x720')
master.resizable(False,False)
bg = Image.open('assets/Background.png').resize((980,720))
bg_tk = ImageTk.PhotoImage(bg)
canvas = tk.Canvas(master,bg='red')
canvas.bg_tk = bg_tk #type: ignore
canvas.pack(fill='both',expand=True)
canvas.create_image(0,0,image=bg_tk,anchor='nw')
start_img = Image.open('assets/play.png').resize((490,270))
start_tk = ImageTk.PhotoImage(start_img)
start_btn = canvas.create_image((480,200),image=start_tk)
editor_img = Image.open('assets/editor.png').resize((490,270))
editor_tk = ImageTk.PhotoImage(editor_img)
editor_btn = canvas.create_image((480,500),image=editor_tk)
platforms.setup(master,canvas)
ladder.setup_ladder(master,canvas)
canvas.tag_bind(start_btn,"<Button-1>",lambda _ : show_levels(master,canvas))
canvas.tag_bind(editor_btn,"<Button-1>",lambda _ : editor.setup_editor(master,bg_tk))
master.mainloop()
