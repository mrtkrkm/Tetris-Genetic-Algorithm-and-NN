import Tetris.Constants as cons
import pygame
import random
from Tetris.Pieces import Pieces

def show_grid(loc):
    '''
    Create grid matrices with background
    Default background is Black

    :param loc:Position of the shape blokes
    '''
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (j, i) in loc:
                color = loc[(j, i)]
                grid[i][j] = color

    return grid


def write_text(font, size, color, text):
    '''
    Add Labels to the surface
    :param font:
    :param size:
    :param color:
    :param text:
    :return: Label. To blit on the surface
    '''
    font = pygame.font.SysFont(font, size)
    label = font.render(text, 1, color)
    return label


def show_score(surface, score):
    '''
    Write score on the surface
    :param surface: Main surface
    :param score: Current Score
    '''
    text = write_text('comicsant', 20, cons.WHITE, 'Score=')
    s_text = write_text('comicsant', 20, cons.WHITE, str(score))
    surface.blit(text, (cons.top_left_x + cons.play_width + 50, cons.top_left_y + 30))
    surface.blit(s_text, (cons.top_left_x + cons.play_width + 50 + text.get_width(),cons.top_left_y + 30))


def starting_window(surface, text):
    '''
    To start the Game function
    :param surface: Main surface
    :param text: Text to show user
    '''
    text = write_text('comicsant', 50, cons.WHITE, text)
    surface.blit(text, (200, 100))
    pygame.display.update()


def show_lines(grid, surface):
    '''
    In order to make playing easy drawing line in the playing area
    :param grid: Main Grid
    :param surface: Main Surface
    '''
    border_color = (255, 0, 0)
    for x in range(len(grid)):
        pygame.draw.line(surface, cons.WHITE, (cons.top_left_x, cons.top_left_y + x * cons.block_size),
                         (cons.top_left_x + cons.play_width, cons.top_left_y + x * cons.block_size))
        for y in range(len(grid[0])):
            if y == 0:
                color = border_color
            else:
                color = cons.WHITE
            pygame.draw.line(surface, color, (cons.top_left_x + y * cons.block_size, cons.top_left_y),
                             (cons.top_left_x + y * cons.block_size, cons.top_left_y + cons.play_height))

    y = y + 1
    pygame.draw.line(surface, (255, 0, 0), (cons.top_left_x + y * cons.block_size, cons.top_left_y),
                     (cons.top_left_x + y * cons.block_size, cons.top_left_y + cons.play_height))


def create_shape():
    '''
    Create a random shape
    :return: Random Shape
    '''
    shape = random.choice(cons.shapes)
    ind = cons.shapes.index(shape)
    color = cons.colors[ind]

    basis_shape = Pieces(5, 0, shape, color)

    return basis_shape


def show_shape(surface, shape, grid):
    '''
    In order to show shape on the Surface
    :param surface: Main Surface
    :param shape: Current Shape
    :param grid: Main Grid
    '''
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pygame.draw.rect(surface, grid[i][j],
                             (cons.top_left_x + j * cons.block_size, cons.top_left_y + i * cons.block_size, cons.block_size, cons.block_size), 0)


def show_next_shape(surface, shape):
    '''
    In order to inform user about the next Shape.
    :param surface: Main Surface
    :param shape: Next Shape
    '''
    text = write_text('comicsant', 30, cons.WHITE, 'Next Shape')

    text_posx = (cons.top_left_x + cons.block_size * 10 + 20)
    text_posy = (cons.play_height) // 3

    surface.blit(text, (text_posx, text_posy))

    shape_pos = get_position(shape)

    for pos in shape_pos:
        (x, y) = pos
        (shape_win_posx, shape_win_posy) = (x * cons.block_size + text_posx - 150, y * cons.block_size + text_posy + 60)
        pygame.draw.rect(surface, shape.color, (shape_win_posx, shape_win_posy, cons.block_size, cons.block_size), 0)

    pygame.display.update()


def clear_rows(grid, loc):
    '''
    After getting point remove the bottom

    Inputs:
    grid: All position of shapes
    loc: COlor of the shapes
    :return: Number of the row that will be deleted and add score
    '''

    y_ps = -1
    inc = 0
    back_color = (0, 0, 0)
    for i in range(len(grid)):
        if back_color not in grid[i]:
            y_ps = i
            inc += 1
            for col in range(len(grid[i])):
                try:
                    del loc[(col, i)]
                except:
                    continue

    if inc > 0:
        for values in sorted(list(loc), key=lambda x: x[1])[::-1]:
            x, y = values
            if y < y_ps:
                new_value = (x, y + inc)
                loc[new_value] = loc.pop(values)

    return inc


def put_shapes(surface, grid, shape):
    '''
    In order to put shapes on the Surface
    :param surface: Main Surface
    :param grid: Main Grid
    :param shape: Current Shape
    '''
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (cons.top_left_x + cons.play_width / 2 - (label.get_width() / 2), 30))

    show_shape(surface, shape, grid)


def check_borders(grid, shape):
    '''
    In order to avoid collision check the borders
    :param grid: Main Grid
    :param shape: Current Shape
    :return: Boolean value which show whether is valid
    '''
    availables = [[(column, row) for column in range(len(grid[0])) if grid[row][column] == (0, 0, 0)] for row in
                  range(len(grid))]
    availables_j = [j for sub in availables for j in sub]

    shape_pos = get_position(shape)

    for pos in shape_pos:
        if pos not in availables_j:
            if pos[1] > -1:
                return False

    return True


def get_position(shape):
    '''
    Convert Basic Shape to positions
    :param shape: Current shape
    :return: (x.y) values of the shape
    '''
    pos = []

    rotation = shape.rotation
    basic_shape = shape.shape
    basic_shape = basic_shape[rotation]

    for i, row in enumerate(basic_shape):
        row = list(row)
        for j, column in enumerate(row):
            if column == '0':
                pos.append((shape.x + j, shape.y + i))


    return pos

def check_end(loc):
    for pos in loc:
        x,y=pos
        if y<1:
            return True
    return False
