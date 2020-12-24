# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\drawing_with_loops.py
# Compiled at: 2020-03-29 18:05:02
# Size of source mod 2**32: 3347 bytes
__doc__ = '\nExample "arcadeplus" library code.\n\nThis example shows how to use functions and loops to draw a scene.\nIt does not assume that the programmer knows how to use classes yet.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.drawing_with_loops\n'
import arcadeplus, random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Drawing With Loops Example'

def draw_background():
    """
    This function draws the background. Specifically, the sky and ground.
    """
    arcadeplus.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3, SCREEN_WIDTH - 1, SCREEN_HEIGHT * 2 / 3, arcadeplus.color.SKY_BLUE)
    arcadeplus.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6, SCREEN_WIDTH - 1, SCREEN_HEIGHT / 3, arcadeplus.color.DARK_SPRING_GREEN)


def draw_bird(x, y):
    """
    Draw a bird using a couple arcs.
    """
    arcadeplus.draw_arc_outline(x, y, 20, 20, arcadeplus.color.BLACK, 0, 90)
    arcadeplus.draw_arc_outline(x + 40, y, 20, 20, arcadeplus.color.BLACK, 90, 180)


def draw_pine_tree(center_x, center_y):
    """
    This function draws a pine tree at the specified location.

    Args:
      :center_x: x position of the tree center.
      :center_y: y position of the tree trunk center.
    """
    arcadeplus.draw_rectangle_filled(center_x, center_y, 20, 40, arcadeplus.color.DARK_BROWN)
    tree_bottom_y = center_y + 20
    point_list = (
     (
      center_x - 40, tree_bottom_y),
     (
      center_x, tree_bottom_y + 100),
     (
      center_x + 40, tree_bottom_y))
    arcadeplus.draw_polygon_filled(point_list, arcadeplus.color.DARK_GREEN)


def main():
    """
    This is the main program.
    """
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.start_render()
    draw_background()
    for bird_count in range(10):
        x = random.randrange(0, SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT / 3, SCREEN_HEIGHT - 20)
        draw_bird(x, y)

    for x in range(45, SCREEN_WIDTH, 90):
        draw_pine_tree(x, SCREEN_HEIGHT / 3)

    for x in range(65, SCREEN_WIDTH, 90):
        draw_pine_tree(x, SCREEN_HEIGHT / 3 - 120)

    arcadeplus.finish_render()
    arcadeplus.run()


if __name__ == '__main__':
    main()