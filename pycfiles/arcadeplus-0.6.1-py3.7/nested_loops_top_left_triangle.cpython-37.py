# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\nested_loops_top_left_triangle.py
# Compiled at: 2020-03-29 18:06:30
# Size of source mod 2**32: 1157 bytes
"""
Example "arcadeplus" library code.

Showing how to do nested loops.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.nested_loops_top_left_triangle
"""
import arcadeplus
COLUMN_SPACING = 20
ROW_SPACING = 20
LEFT_MARGIN = 110
BOTTOM_MARGIN = 110
arcadeplus.open_window(400, 400, 'Complex Loops - Top Left Triangle')
arcadeplus.set_background_color(arcadeplus.color.WHITE)
arcadeplus.start_render()
for row in range(10):
    for column in range(row):
        x = column * COLUMN_SPACING + LEFT_MARGIN
        y = row * ROW_SPACING + BOTTOM_MARGIN
        arcadeplus.draw_circle_filled(x, y, 7, arcadeplus.color.AO)

arcadeplus.finish_render()
arcadeplus.run()