import tkinter as tk
from PIL import Image, ImageTk
import level_selector, editor, platforms, ladder

def setup_menu(master: tk.Tk, canvas: tk.Canvas):
    for callback in level_selector.callbacks:
        master.after_cancel(callback)
    canvas.delete('all')
    bg = Image.open('assets/Background.png').resize((980,720))
    bg_tk = ImageTk.PhotoImage(bg)
    canvas.bg_tk = bg_tk #type: ignore
    canvas.pack(fill='both',expand=True)
    canvas.create_image(0,0,image=bg_tk,anchor='nw')
    start_img = Image.open('assets/play.png').resize((490,270))
    canvas.start_tk = ImageTk.PhotoImage(start_img)
    start_btn = canvas.create_image((480,200),image=canvas.start_tk)
    editor_img = Image.open('assets/editor.png').resize((490,270))
    canvas.editor_tk = ImageTk.PhotoImage(editor_img)
    editor_btn = canvas.create_image((480,500),image=canvas.editor_tk)
    platforms.setup(master,canvas)
    ladder.setup_ladder(master,canvas)
    canvas.tag_bind(start_btn,"<Button-1>",lambda _ : level_selector.show_levels(master,canvas))
    canvas.tag_bind(editor_btn,"<Button-1>",lambda _ : editor.setup_editor(master,canvas.bg_tk))
