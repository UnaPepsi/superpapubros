import tkinter as tk
import player, platforms
master = tk.Tk()
master.geometry('980x720')
canvas = tk.Canvas(master,bg='red')
canvas.pack(fill='both',expand=True)

master.bind('<KeyPress>',player.on_key_press)
master.bind('<KeyRelease>',player.on_key_release)
player.setup_player(master,canvas,0,0)
platforms.setup(master,canvas)
platforms.create_block(200,600)
platforms.create_block(500,550)
player.clock()
master.mainloop()
