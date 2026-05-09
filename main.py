import tkinter as tk
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import menu

master = tk.Tk()
master.geometry('980x720')
master.resizable(False,False)
canvas = tk.Canvas(master,bg='red')
menu.setup_menu(master,canvas)
pygame.mixer.init()
pygame.mixer.music.load('assets/Spy.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)
master.mainloop()

