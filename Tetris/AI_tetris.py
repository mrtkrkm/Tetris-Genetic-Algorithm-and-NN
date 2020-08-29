import GeneticAlgorithm.Steps as genetic
import pygame
import random
import Tetris.Utils as utils
import Tetris.Constants as constants
from Tetris.Pieces import Pieces
from Tetris.BasicShapes import Shapes
import numpy as np

loc={}

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
    loc={}
    grid=utils.show_grid(loc)

    return grid, shape

def adj_x(shapes, rotation):
    shapes.rotation=rotation
    shape_pos = utils.get_position(shapes)
    s_m_width = sorted(shape_pos, key=lambda x: x[0], reverse=True)
    m_width = s_m_width[0][0]
    return  m_width

def ai_playing(number_game, movenumber, weights, nn):
    score=0
    for i in range(number_game):
        grid, shape=starting_values()
        global loc
        loc={}
        for j in range(movenumber):
            max_x, max_y, shape_maxX, shape_maxY = calculate_inputs(grid, shape)
            input=np.array([max_x, max_y, shape_maxX, shape_maxY]).reshape(-1, 4)
            rotate, x = nn.forward(weights, input )
            rotation=np.argmax(rotate)
            x=np.argmax(x)

            # if x + shape_maxX >= 10:
            #     print('fuck')
            #     score -= 20
            #     x=x-shape_maxX
            max_s=(adj_x(shape, rotation%(len(shape.shape)))+x)%10
            x=max_s
            t_score,grid,shape, end=ai_tetris(rotation,x,shape, max_y, shape_maxX, shape_maxY,j)
            score +=t_score
            if end==False:
                break
    return score



def check_ground(shape):
    shape_pos = utils.get_position(shape)
    height_sorted = sorted(shape_pos, key=lambda x: x[1], reverse=True)
    max_height=height_sorted[0][1]
    return 20-max_height


def ai_tetris(rotation, x, shape, maxY, shape_X, shape_y,number):
    pygame.font.init()
    surface = pygame.display.set_mode((constants.S_WIDTH, constants.S_HEIGHT))
    run = True
    second_shape=utils.create_shape()
    global loc
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

        shape.x = x
        shape.rotation = rotation % (len(shape.shape))
        move_to_ground=check_ground(shape)
        move=0
        while move<=move_to_ground-1:
            move +=1
            grid = utils.show_grid(loc)

            utils.show_score(surface, score)
            time += clock.get_rawtime()
            clock.tick()
            # show_shape(surface,first_shape,grid)
            utils.show_lines(grid, surface)
            utils.show_next_shape(surface, second_shape)
            pygame.time.wait(5)
            if not utils.check_borders(grid,shape):
                break
            #shape.y += 1
            position = utils.get_position(shape)
            for pos in position:
                (x, y) = pos
                if y > -1:
                    grid[y][x] = shape.color
            shape.y += 1
            utils.put_shapes(surface, grid, shape)
            pygame.display.update()

        onThe_Ground = True
        shape.y -= 1


        position = utils.get_position(shape)
        if onThe_Ground:
            for pos in position:
                loc_p = (pos[0], pos[1])
                loc[loc_p] = shape.color
            shape = second_shape
            second_shape=utils.create_shape()
            onThe_Ground = False
            score += utils.clear_rows(grid, loc) * 10

        if utils.check_end(loc):
            #score -=50
            score +=(number)*5
            run = False

        #score -=maxY*5

        #pygame.display.update()

        return score,grid,shape, run
