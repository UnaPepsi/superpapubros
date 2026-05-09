import tkinter as tk
import menu

master = tk.Tk()
master.geometry('980x720')
master.resizable(False,False)
canvas = tk.Canvas(master,bg='red')
menu.setup_menu(master,canvas)
master.mainloop()

