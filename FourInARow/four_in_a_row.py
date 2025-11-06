from tkinter import *
from functools import partial
import random
import time

class MainGui:
    root   = Tk()
    all_buttons = [[],[],[],[],[],[]]
    moves = [5, 5, 5, 5, 5, 5, 5]
    player_turn = True
    
    def __init__(self):
        self.draw_board()
        
        self.root.update()
        time.sleep(1)
        
        while True:
            
            # Get indexies for valid moves 
            valid_moves_indeces = [index for index, move in enumerate(self.moves) if move >= 0]
            
            # Valid win state
            if (len(valid_moves_indeces) == 0):
                break
            
            # Make readable variables
            random_move = valid_moves_indeces[random.randrange(0, len(valid_moves_indeces))]
            row_index = self.moves[random_move]
            col_index = random_move
            
            # Actuate target button
            self.alternate_player_turn(self.all_buttons, row_index, col_index)
            
            # Track played move
            self.all_buttons[row_index][col_index] = self.player_turn
            self.moves[col_index] -= 1
            
            self.root.update()
            time.sleep(0.1)
            
            #  or self.check_horizontal(row_index) or self.check_verticles(col_index)
            # Check horizontal
            if (self.check_diagonals(row_index, col_index)):
                break
        
        self.root.mainloop()
            

    def is_win_state(self) -> bool:
        return False
    
    
    def check_horizontal(self, row_index:int) -> bool:
        pieces = self.all_buttons[row_index]
        return self.is_list_containing_4_sequential_bools(pieces)
    
    
    def check_verticles(self, col_index:int) -> bool:
        pieces = [self.all_buttons[row_index][col_index] if isinstance(self.all_buttons[row_index][col_index], bool) else None for row_index in range(0, len(self.all_buttons))]
        return self.is_list_containing_4_sequential_bools(pieces)
    
    
    def check_diagonals(self, row_index:int, col_index:int) -> bool:
        # Check bottom-right to top-left diagonal
        lowest_valid_index_difference = 6 - row_index if (row_index >= col_index) else 5 - col_index 
        x_index = row_index + lowest_valid_index_difference -1
        y_index = col_index + lowest_valid_index_difference -1
        diagonal_pieces = []
        while True:            
            if (x_index < 0 or y_index < 0):
                break
            diagonal_pieces.append(self.all_buttons[x_index][y_index] if isinstance(self.all_buttons[x_index][y_index], bool) else None)
            x_index -= 1
            y_index -= 1
            
        if (self.is_list_containing_4_sequential_bools(diagonal_pieces)):
            return True
            
        # Check bottom-left to top-right diagonal
        
        return self.is_list_containing_4_sequential_bools(diagonal_pieces)

        

    def is_list_containing_4_sequential_bools(self, pieces: list[bool]) -> bool:
        if (len(pieces) < 4):
            return False
        
        count_sequential_valid_pieces = 0
        last_value = self.player_turn
        
        for piece in pieces:
            if count_sequential_valid_pieces == 4:
                return True
            elif piece == None or not isinstance(piece, bool):
                continue
            elif piece == last_value:
                count_sequential_valid_pieces += 1
            else: 
                last_value = not last_value
                count_sequential_valid_pieces = 1
        
        return count_sequential_valid_pieces == 4


    def alternate_player_turn(self, all_buttons_list, x_index, y_index):
        if (isinstance(all_buttons_list[x_index][y_index], bool)):
            return
        self.player_turn = not self.player_turn
        all_buttons_list[x_index][y_index].configure(bg="cornsilk" if self.player_turn == None else "Red" if self.player_turn else "Yellow")
        self.all_buttons[x_index][y_index] = self.player_turn


    def draw_board(self):
        for row_x in range(6):
            for col_y in range(7):
                button_to_add = Button(self.root, command = partial(self.alternate_player_turn, self.all_buttons, row_x, col_y), padx = 25, pady = 25, bg = 'blue')
                self.all_buttons[row_x].append(button_to_add) 
                self.all_buttons[row_x][col_y].grid(row=row_x, column=col_y)

MainGui()
