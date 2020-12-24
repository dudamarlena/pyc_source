# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\happy_face.py
# Compiled at: 2020-03-29 18:05:39
# Size of source mod 2**32: 1391 bytes
"""
Drawing an example happy face

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.happy_face
"""
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