# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\decorator_drawing_example.py
# Compiled at: 2020-03-29 18:04:25
# Size of source mod 2**32: 3353 bytes
__doc__ = '\nExample "arcadeplus" library code.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.decorator_drawing_example\n'
import arcadeplus, random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Drawing With Decorators Example'
window = arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
bird_list = []

def setup():
    create_birds()
    arcadeplus.schedule(update, 0.016666666666666666)
    arcadeplus.run()


def create_birds():
    for bird_count in range(10):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
        bird_list.append([x, y])


def update(_delta_time):
    """
    This is run every 1/60 of a second or so. Do not draw anything
    in this function.
    """
    change_y = 0.3
    for bird in bird_list:
        bird[0] += change_y
        if bird[0] > SCREEN_WIDTH + 20:
            bird[0] = -20


@window.event
def on_draw():
    """
    This is called every time we need to update our screen. About 60
    times per second.

    Just draw things in this function, don't update where they are.
    """
    draw_background()
    draw_birds()
    draw_trees()


def draw_background():
    """
    This function draws the background. Specifically, the sky and ground.
    """
    arcadeplus.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3, SCREEN_WIDTH - 1, SCREEN_HEIGHT * 2 / 3, arcadeplus.color.SKY_BLUE)
    arcadeplus.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6, SCREEN_WIDTH - 1, SCREEN_HEIGHT / 3, arcadeplus.color.DARK_SPRING_GREEN)


def draw_birds():
    for bird in bird_list:
        draw_bird(bird[0], bird[1])


def draw_bird(x, y):
    """
    Draw a bird using a couple arcs.
    """
    arcadeplus.draw_arc_outline(x, y, 20, 20, arcadeplus.color.BLACK, 0, 90)
    arcadeplus.draw_arc_outline(x + 40, y, 20, 20, arcadeplus.color.BLACK, 90, 180)


def draw_trees():
    for x in range(45, SCREEN_WIDTH, 90):
        draw_pine_tree(x, SCREEN_HEIGHT / 3)

    for x in range(65, SCREEN_WIDTH, 90):
        draw_pine_tree(x, SCREEN_HEIGHT / 3 - 120)


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


if __name__ == '__main__':
    setup()