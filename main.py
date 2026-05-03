import tkinter as tk
import player, platforms
master = tk.Tk()
master.geometry('980x720')
canvas = tk.Canvas(master,bg='red')
canvas.pack(fill='both',expand=True)

master.bind('<KeyPress>',player.on_key_press)
master.bind('<KeyRelease>',player.on_key_release)
player.setup_player(master,canvas,0,0)
platforms.setup(master)
platforms.create_block(70,600)
player.clock()
master.mainloop()
