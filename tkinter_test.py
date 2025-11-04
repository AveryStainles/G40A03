from tkinter import *
from functools import partial

# Globals
root   = Tk()
button = []
player_turn = True

def initialize_board() -> None:
    global button
    for a in range( 1, 102 ):
        button.append(a)

def alternate_player_turn(widget, index):
    global player_turn
    player_turn = not player_turn
    widget = widget[index]
    widget.configure(bg="cornsilk" if player_turn == None else "Red" if player_turn else "Yellow")

def draw_board():
    global button
    for row in range(6):
        for col in range(7):
            index = row * 10 + col
            button[index] = Button(
                root, 
                command = partial(alternate_player_turn, button, index), 
                padx = 25, 
                pady = 25, 
                bg = 'blue')
            
            button[index].grid(row=row, column=col)

initialize_board()
draw_board()
button[1 * 10 + 1]

root.mainloop()



