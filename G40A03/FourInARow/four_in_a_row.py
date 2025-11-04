from turtle import *

player_turn = True
previous_move = []
current_move = []

# Skip the turtle drawing animation
tracer(0, 0)

# Setup initial parameters for the turtle screen
def initialize_screen(screen_height = 800, screen_width = 800) -> None:
    screen = Screen()
    screen.setup(screen_width, screen_height)
    bgcolor("Blue")
    draw_board()
    
# Draw a circle at a specified position. 
# If player_turn is not specified, colour should be default background
def draw_circle(x_coordinate, y_coordinate, player_turn = None, radius = 25) -> None:
    penup()
    goto(x_coordinate, y_coordinate)
    pendown()
    fillcolor("cornsilk" if player_turn == None else "Red" if player_turn else "Yellow")
    begin_fill()
    circle(radius)
    end_fill()


starting_x_coordinate = (-72*4)+96
starting_y_coordinate = -150
circle_coordinate_offset = 60

# Draw initial board state for the start of the game
def draw_board():
    x_coordinate =  starting_x_coordinate
    y_coordinate = starting_y_coordinate
    for _ in range(6):
        for _ in range(7):
            # Move coordinate for next column
            draw_circle(x_coordinate, y_coordinate)
            x_coordinate += circle_coordinate_offset
        
        # Move coordinate for next row
        x_coordinate = starting_x_coordinate
        y_coordinate += circle_coordinate_offset
        
def move(x_offset, y_offset):
    global player_turn
    player_turn = not player_turn
    draw_circle(starting_x_coordinate + x_offset, starting_y_coordinate + y_offset, player_turn)
    

def main_loop():
    while True:
        try:
            global player_turn
            print(f"\nPlayer {1 if player_turn else 2}:") 
            
            offset_x = int(input("Enter coordinate x: "))-1
            if (offset_x < 0 or offset_x > 6):
                print(f"\n X coordinate is invalid") 
                continue
            
            offset_y = int(input("Enter coordinate y: "))-1
            if (offset_y < 0 or offset_y > 5):
                print(f"\n Y coordinate is invalid") 
                continue
                
            move(circle_coordinate_offset * offset_x, circle_coordinate_offset * offset_y)
        except:
            print(f"\nThanks for playing!") 
            break

    
initialize_screen()
main_loop()
exitonclick()
