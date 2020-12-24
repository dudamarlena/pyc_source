# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\bouncing_ball.py
# Compiled at: 2020-03-29 18:04:17
# Size of source mod 2**32: 3274 bytes
__doc__ = '\nBounce a ball on the screen, using gravity.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.bouncing_ball\n'
import arcadeplus
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Bouncing Ball Example'
CIRCLE_RADIUS = 20
GRAVITY_CONSTANT = 0.3
BOUNCINESS = 0.9

def draw(_delta_time):
    """
    Use this function to draw everything to the screen.
    """
    arcadeplus.start_render()
    arcadeplus.draw_circle_filled(draw.x, draw.y, CIRCLE_RADIUS, arcadeplus.color.BLACK)
    draw.x += draw.delta_x
    draw.y += draw.delta_y
    draw.delta_y -= GRAVITY_CONSTANT
    if draw.x < CIRCLE_RADIUS:
        if draw.delta_x < 0:
            draw.delta_x *= -BOUNCINESS
        elif draw.x > SCREEN_WIDTH - CIRCLE_RADIUS:
            if draw.delta_x > 0:
                draw.delta_x *= -BOUNCINESS
    elif draw.y < CIRCLE_RADIUS:
        if draw.delta_y < 0:
            if draw.delta_y * -1 > GRAVITY_CONSTANT * 15:
                draw.delta_y *= -BOUNCINESS
            else:
                draw.delta_y *= -BOUNCINESS / 2


draw.x = CIRCLE_RADIUS
draw.y = SCREEN_HEIGHT - CIRCLE_RADIUS
draw.delta_x = 2
draw.delta_y = 0

def main():
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.set_background_color(arcadeplus.color.WHITE)
    arcadeplus.schedule(draw, 0.0125)
    arcadeplus.run()
    arcadeplus.close_window()


if __name__ == '__main__':
    main()