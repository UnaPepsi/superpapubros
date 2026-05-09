import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import level_selector, editor, platforms, ladder
import os

music = True

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
    scores_img = Image.open('assets/scores.png').resize((122,90))
    canvas.scores_img = ImageTk.PhotoImage(scores_img)
    scores_btn = canvas.create_image((899,680),image=canvas.scores_img)
    music_img = Image.open('assets/music.png').resize((80,80))
    canvas.music_img = ImageTk.PhotoImage(music_img)
    music_btn = canvas.create_image((60,670),image=canvas.music_img)
    platforms.setup(master,canvas)
    ladder.setup_ladder(master,canvas)
    canvas.tag_bind(start_btn,"<Button-1>",lambda _ : level_selector.show_levels(master,canvas))
    canvas.tag_bind(editor_btn,"<Button-1>",lambda _ : editor.setup_editor(master,canvas.bg_tk))
    canvas.tag_bind(scores_btn,"<Button-1>",lambda _ : show_scores(master))
    canvas.tag_bind(music_btn,"<Button-1>",lambda _ : toggle_music())

def show_scores(m: tk.Tk):
    if not os.path.isfile('scores.txt'):
        messagebox.showerror(message='No hay puntuaciones registradas')
        return
    tl = tk.Toplevel(m)
    tl.resizable(False,False)
    tl.title('10 Puntajes más altos')
    lsbox = tk.Listbox(tl)
    with open('scores.txt','r') as f:
        scores = []
        for line in f.readlines():
            score,name = line.removesuffix('\n').split(',',1)
            scores.append((int(score),name))
        scores.sort(key=lambda score: score[0],reverse=True)
        for i,score in enumerate(scores[:10]):
            lsbox.insert(i,f'{i+1}. {score[1]}: {score[0]}')
    width = max(len(str(scr[0]))+len(scr[1]) for scr in scores) + 2
    lsbox.configure(width=width)
    lsbox.pack()

def toggle_music():
    global music
    if music: pygame.mixer.music.pause()
    else: pygame.mixer.music.unpause()
    music = not music
