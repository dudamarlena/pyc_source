# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\bouncing_rectangle.py
# Compiled at: 2020-03-29 18:04:46
# Size of source mod 2**32: 3180 bytes
"""
This simple animation example shows how to bounce a rectangle
on the screen.

It assumes a programmer knows how to create functions already.

It does not assume a programmer knows how to create classes. If you do know
how to create classes, see the starting template for a better example:

Or look through the examples showing how to use Sprites.

A video walk-through of this example is available at:
https://vimeo.com/168063840

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.bouncing_rectangle

"""
import arcadeplus
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Bouncing Rectangle Example'
RECT_WIDTH = 50
RECT_HEIGHT = 50

def on_draw(delta_time):
    """
    Use this function to draw everything to the screen.
    """
    arcadeplus.start_render()
    arcadeplus.draw_rectangle_filled(on_draw.center_x, on_draw.center_y, RECT_WIDTH, RECT_HEIGHT, arcadeplus.color.ALIZARIN_CRIMSON)
    on_draw.center_x += on_draw.delta_x * delta_time
    on_draw.center_y += on_draw.delta_y * delta_time
    if on_draw.center_x < RECT_WIDTH // 2 or on_draw.center_x > SCREEN_WIDTH - RECT_WIDTH // 2:
        on_draw.delta_x *= -1
    if on_draw.center_y < RECT_HEIGHT // 2 or on_draw.center_y > SCREEN_HEIGHT - RECT_HEIGHT // 2:
        on_draw.delta_y *= -1


on_draw.center_x = 100
on_draw.center_y = 50
on_draw.delta_x = 115
on_draw.delta_y = 130

def main():
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.set_background_color(arcadeplus.color.WHITE)
    arcadeplus.schedule(on_draw, 0.0125)
    arcadeplus.run()


if __name__ == '__main__':
    main()