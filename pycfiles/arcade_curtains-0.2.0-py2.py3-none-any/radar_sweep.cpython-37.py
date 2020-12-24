# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\radar_sweep.py
# Compiled at: 2020-03-29 18:07:23
# Size of source mod 2**32: 1984 bytes
__doc__ = '\nThis animation example shows how perform a radar sweep animation.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.radar_sweep\n'
import arcadeplus, math
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Radar Sweep Example'
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250

def on_draw(_delta_time):
    """ Use this function to draw everything to the screen. """
    on_draw.angle += RADIANS_PER_FRAME
    x = SWEEP_LENGTH * math.sin(on_draw.angle) + CENTER_X
    y = SWEEP_LENGTH * math.cos(on_draw.angle) + CENTER_Y
    arcadeplus.start_render()
    arcadeplus.draw_line(CENTER_X, CENTER_Y, x, y, arcadeplus.color.OLIVE, 4)
    arcadeplus.draw_circle_outline(CENTER_X, CENTER_Y, SWEEP_LENGTH, arcadeplus.color.DARK_GREEN, 10)


on_draw.angle = 0

def main():
    arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.set_background_color(arcadeplus.color.BLACK)
    arcadeplus.schedule(on_draw, 0.0125)
    arcadeplus.run()
    arcadeplus.close_window()


if __name__ == '__main__':
    main()