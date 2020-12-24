# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\happy_face.py
# Compiled at: 2020-03-29 18:05:39
# Size of source mod 2**32: 1391 bytes
__doc__ = '\nDrawing an example happy face\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.happy_face\n'
import arcadeplus
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Happy Face Example'
arcadeplus.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcadeplus.set_background_color(arcadeplus.color.WHITE)
arcadeplus.start_render()
x = 300
y = 300
radius = 200
arcadeplus.draw_circle_filled(x, y, radius, arcadeplus.color.YELLOW)
x = 370
y = 350
radius = 20
arcadeplus.draw_circle_filled(x, y, radius, arcadeplus.color.BLACK)
x = 230
y = 350
radius = 20
arcadeplus.draw_circle_filled(x, y, radius, arcadeplus.color.BLACK)
x = 300
y = 280
width = 120
height = 100
start_angle = 190
end_angle = 350
arcadeplus.draw_arc_outline(x, y, width, height, arcadeplus.color.BLACK, start_angle, end_angle, 10)
arcadeplus.finish_render()
arcadeplus.run()