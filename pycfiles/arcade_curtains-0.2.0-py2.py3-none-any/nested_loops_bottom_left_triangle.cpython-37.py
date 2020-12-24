# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\nested_loops_bottom_left_triangle.py
# Compiled at: 2020-03-29 18:06:21
# Size of source mod 2**32: 1168 bytes
__doc__ = '\nExample "arcadeplus" library code.\n\nShowing how to do nested loops.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.nested_loops_bottom_left_triangle\n'
import arcadeplus
COLUMN_SPACING = 20
ROW_SPACING = 20
LEFT_MARGIN = 110
BOTTOM_MARGIN = 110
arcadeplus.open_window(400, 400, 'Complex Loops - Bottom Left Triangle')
arcadeplus.set_background_color(arcadeplus.color.WHITE)
arcadeplus.start_render()
for row in range(10):
    for column in range(10 - row):
        x = column * COLUMN_SPACING + LEFT_MARGIN
        y = row * ROW_SPACING + BOTTOM_MARGIN
        arcadeplus.draw_circle_filled(x, y, 7, arcadeplus.color.AO)

arcadeplus.finish_render()
arcadeplus.run()