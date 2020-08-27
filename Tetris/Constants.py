from Tetris.BasicShapes import Shapes as bs


S_WIDTH=800
S_HEIGHT=600
play_width=300
play_height=600
block_size=30

WHITE=(255,255,255)

top_left_x = (S_WIDTH - play_width) // 2
top_left_y = S_HEIGHT - play_height

shapes=[bs.S, bs.Z, bs.O, bs.I, bs.J, bs.L, bs.T]
colors=[(255,0,0),(0,255,0),(0,0,255),(128,128,128),(255,255,255),(128,0,128),(0,128,128)]