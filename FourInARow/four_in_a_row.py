import tkinter as tk
from functools import partial
import random
import time

class Game:
    root = tk.Tk()
    all_buttons = [[],[],[],[],[],[]]
    moves = [5, 5, 5, 5, 5, 5, 5]
    player_turn = True
    display_text = tk.StringVar()
    label: tk.Label = tk.Label(root, textvariable=display_text, bg="Black", width=21, font=("Arial", 24, "bold"), fg=f"{"Red" if player_turn else "Yellow"}")
    is_paused = True
    speed = 0.75
    
    def __init__(self):
        self.display_text.set("Press start to being!")
        self.label.grid(row=7, column=0, columnspan= 7)
        self.run_simulation()
    
    
    def run_simulation(self):
        self.event_listeners()
        self.draw_board()
        self.root.update()
        
        while True:
            time.sleep(self.speed)
            self.root.update()
            
            if (self.is_paused):
                continue
            
            # Get indexies for valid moves 
            valid_moves_indeces = [index for index, move in enumerate(self.moves) if move >= 0]
            
            # Valid win state
            if (len(valid_moves_indeces) == 0):
                self.player_turn = None
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
            
            if (self.is_win_state(row_index, col_index)):
                break
        
        self.display_game_over_text()
        
        self.root.mainloop()


    def is_win_state(self, row_index:int, col_index:int) -> bool:
        return self.check_horizontal(row_index) or self.check_verticles(col_index) or self.check_diagonals(row_index, col_index) 
    
    
    def check_horizontal(self, row_index:int) -> bool:
        row_pieces = self.all_buttons[row_index]
        return self.is_list_containing_4_sequential_bools(row_pieces)
    
    
    def check_verticles(self, col_index:int) -> bool:
        col_pieces = [self.all_buttons[row_index][col_index] if isinstance(self.all_buttons[row_index][col_index], bool) else None for row_index in range(0, len(self.all_buttons))]
        return self.is_list_containing_4_sequential_bools(col_pieces)
    
    
    def check_diagonals(self, row_index:int, col_index:int) -> bool:
        # Check bottom-right to top-left diagonal
        lowest_valid_index_difference: int = 5 - row_index if (row_index >= col_index) else 6 - col_index 
        x_index: int = row_index + lowest_valid_index_difference 
        y_index: int = col_index + lowest_valid_index_difference 
        diagonal_pieces: list[bool | None | tk.Button] = []
        while True:            
            if (x_index < 0 or y_index < 0):
                break
            diagonal_pieces.append(self.all_buttons[x_index][y_index] if isinstance(self.all_buttons[x_index][y_index], bool) else None)
            x_index -= 1
            y_index -= 1
            
        if (self.is_list_containing_4_sequential_bools(diagonal_pieces)):
            return True
            
        # Check bottom-left to top-right diagonal
        x_index: int = 5
        y_index: int = col_index - (5-row_index)
        diagonal_pieces: list[bool | None | tk.Button] = []
        while True:            
            if (x_index < 0 or y_index > 6):
                break
            elif (not y_index < 0):
                diagonal_pieces.append(self.all_buttons[x_index][y_index] if isinstance(self.all_buttons[x_index][y_index], bool) else None)
            
            x_index -= 1
            y_index += 1
            
        return self.is_list_containing_4_sequential_bools(diagonal_pieces)
            

    def is_list_containing_4_sequential_bools(self, pieces: list[bool]) -> bool:
        if (len(pieces) < 4):
            return False
        
        count_sequential_valid_pieces: int = 0
        last_value: bool = self.player_turn
        
        for piece in pieces:
            if count_sequential_valid_pieces == 4:
                return True
            elif piece == None or not isinstance(piece, bool):
                count_sequential_valid_pieces: int = 0
                continue
            elif piece == last_value:
                count_sequential_valid_pieces += 1
            else: 
                last_value: bool = not last_value
                count_sequential_valid_pieces: int = 1
        
        return count_sequential_valid_pieces == 4


    def display_game_over_text(self):
        self.display_text.set(f"{"Draw!" if self.player_turn == None else ("Red" if self.player_turn else "Yellow") + " wins!"}")
        self.label: tk.Label = tk.Label(self.root, textvariable=self.display_text, bg="Black", width=21, font=("Arial", 24, "bold"), fg=f"{"Red" if self.player_turn else "Yellow"}")
        self.label.grid(row=7, column=0, columnspan= 7)


    def event_listeners(self):
        self.root.bind("r", lambda _: self.clear())
        self.root.bind("q", lambda _: self.root.destroy())
        self.root.bind("p", lambda _: self.pause())
        self.root.bind("s", lambda _: self.start())
        self.root.bind("+", lambda _: self.increase_speed())
        self.root.bind("-", lambda _: self.decrease_speed())


    def increase_speed(self) -> None:
        self.speed: float = self.speed if self.speed <= 0 else self.speed - 0.25
        self.display_text.set(f"Speed: {2 - self.speed}x")


    def decrease_speed(self) -> None:
        self.speed: float = self.speed if self.speed >= 2 else self.speed + 0.25
        self.display_text.set(f"Speed: {2 - self.speed}x")
    
    
    def pause(self) -> None:
        self.display_text.set("Game pause!") 
        self.is_paused: bool = True
        
        
    def start(self) -> None:
        self.display_text.set("Game start!") 
        self.is_paused: bool = False


    def clear(self) -> None:
        self.all_buttons: list[list[bool | tk.Button | None]] = [[],[],[],[],[],[]]
        self.moves: list[int] = [5, 5, 5, 5, 5, 5, 5]
        self.player_turn: bool = True
        self.run_simulation()
        self.display_text.set("")


    def alternate_player_turn(self, all_buttons_list, x_index, y_index) -> None:
        if (isinstance(all_buttons_list[x_index][y_index], bool)):
            return
        self.player_turn: bool = not self.player_turn
        
        all_buttons_list[x_index][y_index].configure(bg="cornsilk" if self.player_turn == None else "Red" if self.player_turn else "Yellow")
        self.all_buttons[x_index][y_index] = self.player_turn


    def draw_board(self) -> None:
        self.root.title("4 in a row")
        for row_x in range(6):
            for col_y in range(7):
                button_to_add: tk.Button = tk.Button(self.root, command = partial(self.alternate_player_turn, self.all_buttons, row_x, col_y), padx = 25, pady = 25, bg = 'blue')
                self.all_buttons[row_x].append(button_to_add) 
                self.all_buttons[row_x][col_y].grid(row=row_x, column=col_y)
        self.root.update()


if __name__ == "__main__":
    Game()
