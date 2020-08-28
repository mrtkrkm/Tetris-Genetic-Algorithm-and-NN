import GA.Steps as genetic
import pygame
import random
import Tetris.Utils as utils
import Tetris.Constants as constants
from Tetris.Pieces import Pieces
from Tetris.BasicShapes import Shapes
import numpy as np



def calculate_inputs(grid,shape):
    max_x=0
    max_y=0
    max_shapex=0
    max_shapey=0

    for i in range(len(grid)):
        count_x=0
        for j in range(len(grid[0])):
            if grid[i][j]!=(0,0,0):
                count_x +=1
        if count_x>max_x:
            max_x=count_x

    for i in range(len(grid[0])):
        count_y=0
        for j in range(len(grid)):
            if grid[j][i]!=(0,0,0):
                count_y +=1
        if count_y>max_y:
            max_y=count_y

    basic_shape=shape.shape

    for i in range(len(basic_shape)):
        shape.rotation=i
        shape_pos=utils.get_position(shape)

        height_sorted=sorted(shape_pos, key=lambda x:x[1], reverse=True)
        max_height=(height_sorted[0][1]-height_sorted[len(height_sorted)-1][1])+1

        width_sorted=sorted(shape_pos, key=lambda x:x[0], reverse=True)
        max_width=(width_sorted[0][0]-width_sorted[len(width_sorted)-1][0])+1

        if max_height>max_shapey:
            max_shapey=max_height
        if max_width>max_shapex:
            max_shapex=max_width

    return max_x, max_y, max_shapex, max_shapey



def starting_values():
    shape=utils.create_shape()
    global loc
    loc={}
    grid=utils.show_grid(loc)

    return grid, shape


def ai_playing(number_game, movenumber, weights, nn):
    score=0
    for i in range(number_game):
        grid, shape=starting_values()
        for j in range(movenumber):
            max_x, max_y, shape_maxX, shape_maxY = calculate_inputs(grid, shape)
            input=np.array([max_x, max_y, shape_maxX, shape_maxY]).reshape(-1, 4)
            rotate, x = nn.forward(weights, input )
            rotation=np.argmax(rotate)
            x=np.argmax(x)

            if x + max_x > 10:
                score += 20
                x=2
            t_score,grid,shape, end=ai_tetris(rotation,x,shape, max_y, shape_maxX, shape_maxY)
            score +=t_score
            if end:
                break




    return score



def ai_play(surface, popsize, movenumber,weights):
    run=True
    loc = {}
    first_shape = utils.create_shape()
    second_shape=utils.create_shape()
    surface.fill((0,0,0))
    rotation=0
    grid=utils.show_grid(loc)
    onThe_Ground=False
    time=0
    clock=pygame.time.Clock()
    score=0



    while run:

        grid=utils.show_grid(loc)
        utils.show_score(surface, score)
        time +=clock.get_rawtime()
        clock.tick()
        #show_shape(surface,first_shape,grid)
        utils.show_lines(grid, surface)
        utils.show_next_shape(surface,second_shape)
        if time/1000>0.3:
            time=0
            first_shape.y += 1
            if not utils.check_borders(grid, first_shape):
                first_shape.y -= 1
                onThe_Ground = True

        #max_x, max_y, shape_maxX, shape_maxY=calculate_inputs(surface, grid, first_shape)
        #rotate, x=ff.forward(weights,np.array([max_x, max_y,shape_maxX,shape_maxY]).reshape(-1,7))


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    first_shape.y +=1
                    if not utils.check_borders(grid, first_shape):
                        first_shape.y -=1
                        onThe_Ground=True
                if event.key==pygame.K_RIGHT:
                    first_shape.x+=1
                    if not utils.check_borders(grid, first_shape):
                        first_shape.x -=1
                if event.key==pygame.K_LEFT:
                    first_shape.x -=1
                    if not utils.check_borders(grid, first_shape):
                        first_shape.x +=1
                if event.key==pygame.K_UP:
                    rotation +=1
                    if rotation>len(first_shape.shape)-1:
                        rotation =0
                    first_shape.rotation=rotation
        position=utils.get_position(first_shape)
        for pos in position:
            (x,y)=pos
            grid[y][x]=first_shape.color
        utils.put_shapes(surface,grid,first_shape)
        if onThe_Ground:
            for pos in position:
                loc_p=(pos[0], pos[1])
                loc[loc_p]=first_shape.color
            first_shape=second_shape
            second_shape=utils.create_shape()
            onThe_Ground=False
            score +=utils.clear_rows(grid, loc)*10
        if utils.check_end(loc):
            run=False
    pygame.display.quit()


def ai_tetris(rotation, x, shape, maxY, shape_X, shape_y):
    pygame.font.init()
    score=0
    surface = pygame.display.set_mode((constants.S_WIDTH, constants.S_HEIGHT))
    run = True
    second_shape=utils.create_shape()
    loc = {}
    surface.fill((0, 0, 0))
    grid = utils.show_grid(loc)
    onThe_Ground = False
    time = 0
    clock = pygame.time.Clock()
    score = 0

    while run:
        surface.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        shape.x=x
        shape.rotation=rotation%(len(shape.shape))

        position = utils.get_position(shape)
        for pos in position:
            (x, y) = pos
            grid[y][x] = shape.color
        utils.put_shapes(surface, grid, shape)

        if onThe_Ground:
            for pos in position:
                loc_p = (pos[0], pos[1])
                loc[loc_p] = shape.color
            shape = second_shape
            second_shape = utils.create_shape()
            onThe_Ground = False
            score += utils.clear_rows(grid, loc) * 10

        if utils.check_end(loc):
            score -=150
            run = False

        score -=maxY*5

        pygame.display.update()

        return score,grid,shape, run


def run_game(window, popsize, movenumber, weights):
    run=True

    while run:
        window.fill((0,0,0))
        utils.starting_window(window,'please press a button')
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                ai_play(window, popsize, movenumber, weights)
        pygame.display.update()
    pygame.display.quit()

def main_func(popsize, movenumber, weights):
    pygame.font.init()

    window=pygame.display.set_mode((constants.S_WIDTH, constants.S_HEIGHT))
    run_game(window, popsize, movenumber, weights)
