# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\drawing_with_functions.py
# Compiled at: 2020-03-29 18:04:58
# Size of source mod 2**32: 2834 bytes
"""
Example "arcadeplus" library code.

This example shows how to use functions to draw a scene.
It does not assume that the programmer knows how to use classes yet.

A video walk-through of this code is available at:
https://vimeo.com/167296062

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.drawing_with_functions
"""
import arcadeplus
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Drawing With Functions Example'

def draw_background():
    """
    This function draws the background. Specifically, the sky and ground.
    """
    arcadeplus.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT * 0.3333333333333333, arcadeplus.color.SKY_BLUE)
    arcadeplus.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT / 3, 0, arcadeplus.color.DARK_SPRING_GREEN)


def draw_bird(x, y):
    """
    Draw a bird using a couple arcs.
    """
    arcadeplus.draw_arc_outline(x, y, 20, 20, arcadeplus.color.BLACK, 0, 90)
    arcadeplus.draw_arc_outline(x + 40, y, 20, 20, arcadeplus.color.BLACK, 90, 180)


def draw_pine_tree(x, y):
    """
    This function draws a pine tree at the specified location.
    """
    arcadeplus.draw_triangle_filled(x + 40, y, x, y - 100, x + 80, y - 100, arcadeplus.color.DARK_GREEN)
    arcadeplus.draw_lrtb_rectangle_filled(x + 30, x + 50, y - 100, y - 140, arcadeplus.color.DARK_BROWN)


def main():
    """
    This is the main program.
    """
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.start_render()
    draw_background()
    draw_pine_tree(50, 250)
    draw_pine_tree(350, 320)
    draw_bird(70, 500)
    draw_bird(470, 550)
    arcadeplus.finish_render()
    arcadeplus.run()


if __name__ == '__main__':
    main()