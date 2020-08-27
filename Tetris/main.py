import Tetris.Utils as utils
import pygame
import Tetris.Constants as constants

def game_functions(surface):
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
    #draw_grid(surface)
    while run:
        #starting_window(surface, 'inside game')
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

    pygame.display.quit()


def run_game(window):
    run=True

    while run:
        window.fill((0,0,0))
        utils.starting_window(window,'please press a button')
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                game_functions(window)
        pygame.display.update()
    pygame.display.quit()

def main_func():
    pygame.font.init()

    window=pygame.display.set_mode((constants.S_WIDTH, constants.S_HEIGHT))
    run_game(window)