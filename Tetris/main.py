import pygame
import random
from Tetris.BasicShapes import Shapes as bs
from Tetris.Pieces import Pieces

pygame.font.init()

S_WIDTH=800
S_HEIGHT=600
play_width=300
play_height=600
block_size=30

top_left_x = (S_WIDTH - play_width) // 2
top_left_y = S_HEIGHT - play_height

shapes=[bs.S, bs.Z, bs.O, bs.I, bs.J, bs.L, bs.T]
colors=[(255,0,0),(0,255,0),(0,0,255),(128,128,128),(255,255,255),(128,0,128),(0,128,128)]

def show_grid(loc):
    grid=[[(0,0,0) for _ in range(10) ]for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i,j) in loc:
                color=loc[(i,j)]
                grid[i][j]=color
    
    return grid
            
def create_shape():
    shape=random.choice(shapes)
    basis_shape=Pieces(5,0,shape,colors[shapes.index[shape]])

    return basic_shape

def clear_rows(filled_pos, grid):
    '''
    After getting point remove the bottom

    Inputs:
    filled_pos= All position of shapes
    '''
    
    y_ps=-1
    inc=0
    back_color=(0,0,0)
    for i in range(grid):
        if back_color not in grid[i]:
            y_ps=i
            inc +=1

    if inc>0:
        




def put_shapes(surface,grid, shape):
    position=get_position(shape)

    for i in range(grid):
        for j in range(grid[0]):
            pygame.draw.rect(surface, grid[i][j],(top_left_x+j*block_size, top_left_y+i*block_size, block_size, block_size),0)
    



def check_borders():
    pass

def get_position(shape):
    pos=[]

    shape=shape[shape.rotation]

    for i,row in enumerate(len(shape)):
        row=list(row)
        for j,column in enumerate(len(row)):
            if column=='0':
                pos.append((i,j))
    
    return pos


def game_functions():
    pass


def run_game(window):
    run=True
    while run:
        window.fill((254,255,255))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                grid=show_grid()
                shape=create_shape()
                put_shapes(window, grid, shape)
                #game_functions()
    
    pygame.display.quit()


def main_func():
    window=pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    run_game(window)

