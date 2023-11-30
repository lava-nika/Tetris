import pygame
import random

pygame.font.init() # Initializes fonts and makes them available for use
pygame.init()

pygame.mixer.music.load("epic.wav")
pygame.mixer.music.set_volume(0.2)
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

Z = [['.....',
      '.....', 
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00.',
      '.0...',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0.',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#GLOBAL VARIABLES
 
shapes = [S, Z, I, O, J, L, T] # A list of all 7 shapes of pieces
 
shape_colors = [ (0, 204, 0) , (255, 0, 127) , (102, 0, 204) , (204, 0, 0) , (0, 128, 255) , (255, 128, 0) , (255, 255, 0) ] # A list depicting the colour (in RGB value) for corresponding shapes of pieces.
 
block_size = 30 # Size of each block on the grid that we will make

w_height = 800
w_width = 700

play_width = 300 # Area where blocks will be falling
play_height = 600 

top_left_x = (w_width - play_width)//2
top_left_y = (w_height - play_height)

score = 0
 
#CLASS DEFINITION
 
class Piece:
    x = 10 # Number of columns, set default to 10
    y = 20 # Number of rows, set default to 20
    shape = 0 # Shape of piece, set default to 0
    color = () # Color of shape
    rotation = 0 #Current orientation/rotation, default set to 0
    # This is a constructor
    def __init__(self, column, row, shape):
      # The values in parameters are assigned to the new object of type 'Piece'
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
         
#FUNCTION DEFINITIONS

def draw_text_middle(text,size,color,surface):

    # Assign the font
    font = pygame.font.SysFont('comicsans', size, bold = True) #default is non bolded

    # Render the font on the text
    label = font.render(text,1,color) # Here, no. of times it repeats = 1. This function applies to the text that we want to display

    # Display on screen, find x and y coord of middle of screen
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
     
     
def create_grid(locked_positions):
    grid = [[(0,0,0) for x in range(10)] for y in range(20)] # Colors entire 20 x 10 grid in black
     
    # These nested loops color up all locked positions     
    for i in range (len(grid)): 
        for j in range (len(grid[i])):
               if(j,i) in locked_positions: 
                        c = locked_positions[(j,i)]
                        grid[i][j] = c
    return grid

def get_shape():
    newPiece = Piece(5,0,random.choice(shapes)) # For it to fall from middle of screen
    return newPiece

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    #loop over the formatted grid
    i=0
    for line in format:
         row = list(line)
         j = 0
         for column in row:
             if column=='0':
                 positions.append((piece.x + j, piece.y + i))
             j+=1
         i+=1
    k = 0
    for pos in positions:
        positions[k] = (pos[0] - 2, pos[1] - 4) #from k=0 it is optional code, directly return positions
        k+=1
         
    return positions
     

def valid_space( piece, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(piece)

    # Check if the block lies in a position that is not accepted (not valid)
    for pos in formatted:
         if pos not in accepted_positions:
             if pos[1] > -1:
                 return False
    return True
     
def update_score(surface):
    text = "Score : " + str(score)

    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(text, 1, (250,50,100))

    sx = top_left_x + play_width + 40
    sy = top_left_y + play_height/2 - 100

    surface.blit( label, (sx + 10, sy + 150 ))

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (250,50,100))

    sx = top_left_x + play_width + 50 # + 50 by trial and error
    sy = top_left_y + play_height/2 - 100 # trial and error

    format = piece.shape[piece.rotation % len(piece.shape)]

    i = 0
    for line in format:
        row = list(line)
        j = 0
        # Traverse through each string
        for column in row:
             if column == '0':
                 # Draw the next_piece
                 pygame.draw.rect(surface, piece.color, (sx + j*30, sy + i*30, 30, 30), 0)
             j+=1
        i+=1
         
    surface.blit(label, (sx + 10, sy - 30))
    update_score(surface)
     
def check_lost(positions):

    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False
     

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y

    for i in range(row):
        pygame.draw.line(surface, (117, 77, 52), (sx, sy+i*30), (sx + play_width, sy + i*30))

        for j in range(col):
            # Draw Vertical Lines
            pygame.draw.line(surface, (117, 77, 52), (sx + j*30, sy), (sx +j*30, sy + play_height))
             


def draw_window(surface):

    surface.fill((0,0,0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS',1,(255,255,255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range( len(grid) ):
        for j in range( len(grid[i] )):
            # draw the block
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*30, top_left_y + i*30, block_size, block_size), 0)

    draw_grid(surface, 20, 10)

    pygame.draw.rect(surface, (0, 255, 145), (top_left_x, top_left_y, play_width, play_height), 5)


def clear_rows(grid, locked):
    global score
    # We store the number of rows to shift down in inc
    inc = 0
    
    for i in range(len(grid)-1, -1, -1): # Start traversal from bottom of grid
        row = grid[i]
        # Check if there is any empty position(block) in this row
        if (0, 0, 0) not in row:
            inc += 1
            # Clear this row, save the index into ind
            ind = i
            for j in range(len(row)):
                try:
                    del locked[ (j, i) ]
                except:
                    continue
                
    if inc > 0:
        # Sort the locked position, store into temp
        temp = sorted( list( locked ), key=lambda x: x[1])
        #Traverse temp in reverse direction
        for key in temp[::-1]:
            x,y = key
            # If the y coordinate of this position is less than ind
            if y < ind:
                # Update the y coordinate
                newKey = (x, y+inc)
                # Remove the previous locked position from the list
                locked[newKey] = locked.pop(key)

        score+=10
        

def play(): #to define our play area/grid
    global grid

    pygame.mixer.music.play(-1)

    locked_positions = {} # This keeps a track of any places already occupied by a colored block/piece

    # This creates a dictionary, defines key-value pairs
    # d = {}
    # d = {'apple' = 'red', 'orange' = 'orange', 'banana' = 'yellow'}
    # d['apple'] = 'green'
    # similar to lists only
    # here black is not locked
    # locked_positions = {(0,1) : (0,0,0), (15,9): (255,0,0)}
    # Keys are x and y coord and values are the colors assigned to it

    grid = create_grid(locked_positions)
    
    change_piece = False # True when current piece touches the ground. To keep track it is reqd

    run = True # To keep the pieces falling until user loses the game

    current_piece = get_shape()

    next_piece = get_shape()

    clock = pygame.time.Clock()

    fall_time = 0 # When this exceeds a certain value (specified below), y coord is increased by 1

    while run:
        fall_speed = 0.27

        grid = create_grid(locked_positions) # Updates the grid to color the current piece that is falling and show it on the screen. So we need to create the grid again.

        fall_time += clock.get_rawtime() # Returns raw time of your computer system time

        clock.tick() # Needs to move 1 sec ahead

        if fall_time/1000 >= fall_speed: # /1000 to convert to ms
            fall_time = 0
            current_piece.y += 1 # Fall one position down

            if not(valid_space(current_piece,grid)) and current_piece.y > 0: # Should freeze on hitting/overlapping with another piece
                   current_piece.y -= 1 # Reverse the changes
                   change_piece = True # Next piece will fall
                   
        for event in pygame.event.get():
            # Check if user clicks on CROSS button to QUIT
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.music.stop()
                pygame.display.quit()
                quit() #to close the window automatically, this is a python function, not pygame func

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                     current_piece.x += 1
                     if not valid_space(current_piece, grid):
                         current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP: #change rotation
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape) # eg len returns 3 for T (0,1,2,3)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y>-1:
                grid[y][x] = current_piece.color #we are coloring the piece wherever the piece is

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
                
            current_piece = next_piece
            next_piece = get_shape()

            change_piece = False

            clear_rows(grid, locked_positions)

            

        draw_window(window)
        draw_next_shape(next_piece, window)

        pygame.display.update() #need to execute everytime we draw something on screen

        if check_lost(locked_positions):
            run = False

    window.fill((0,0,0))
    pygame.mixer.music.stop()
    draw_text_middle("You Lost!", 80, (255,140,0), window)

    pygame.display.update()
    pygame.time.delay(2000)
 
    
 
def game():
    run = True

    while run:
        window.fill ((0,0,0)) # Fills entire window black

        draw_text_middle("Press any key to begin!", 60, (150,255,0), window)

        pygame.display.update()

        for event in pygame.event.get(): # Returns a list of events which occurred (eg. left arrow key and right arrow key in this case)

            if event.type == pygame.KEYDOWN: #when any key is pressed
                play() # User defined, to start playing the game

            if event.type == pygame.QUIT:
                run = False

    pygame.quit() # Closes game window, when we come out of the while loop

      

#DRIVER CODE

window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("TETRIS")

game()



