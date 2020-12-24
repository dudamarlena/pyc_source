# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\isometric.py
# Compiled at: 2020-03-29 14:03:52
# Size of source mod 2**32: 2034 bytes
from arcadeplus import ShapeElementList
from arcadeplus.buffered_draw_commands import create_line

def isometric_grid_to_screen(tile_x, tile_y, width, height, tile_width, tile_height):
    screen_x = tile_width * tile_x // 2 + height * tile_width // 2 - tile_y * tile_width // 2
    screen_y = (height - tile_y - 1) * tile_height // 2 + width * tile_height // 2 - tile_x * tile_height // 2
    return (screen_x, screen_y)


def screen_to_isometric_grid(screen_x, screen_y, width, height, tile_width, tile_height):
    x2 = (1 / tile_width * screen_x / 2 - 1 / tile_height * screen_y / 2 + width / 2) * 2 - (width / 2 + 0.5)
    y2 = height - 1 - ((1 / tile_width * screen_x / 2 + 1 / tile_height * screen_y / 2) * 2 - (width / 2 + 0.5))
    x2 = round(x2)
    y2 = round(y2)
    return (x2, y2)


def create_isometric_grid_lines(width, height, tile_width, tile_height, color, line_width):
    shape_list = ShapeElementList()
    for tile_row in range(-1, height):
        tile_x = 0
        start_x, start_y = isometric_grid_to_screen(tile_x, tile_row, width, height, tile_width, tile_height)
        tile_x = width - 1
        end_x, end_y = isometric_grid_to_screen(tile_x, tile_row, width, height, tile_width, tile_height)
        start_x -= tile_width // 2
        end_y -= tile_height // 2
        line = create_line(start_x, start_y, end_x, end_y, color, line_width=line_width)
        shape_list.append(line)

    for tile_column in range(-1, width):
        tile_y = 0
        start_x, start_y = isometric_grid_to_screen(tile_column, tile_y, width, height, tile_width, tile_height)
        tile_y = height - 1
        end_x, end_y = isometric_grid_to_screen(tile_column, tile_y, width, height, tile_width, tile_height)
        start_x += tile_width // 2
        end_y -= tile_height // 2
        line = create_line(start_x, start_y, end_x, end_y, color, line_width=line_width)
        shape_list.append(line)

    return shape_list