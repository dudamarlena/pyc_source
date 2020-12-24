# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\drawing_primitives.py
# Compiled at: 2020-03-29 18:25:43
# Size of source mod 2**32: 6061 bytes
__doc__ = '\nExample "arcadeplus" library code.\n\nThis example shows the drawing primitives and how they are used.\nIt does not assume the programmer knows how to define functions or classes\nyet.\n\n\nA video explaining this example can be found here:\nhttps://vimeo.com/167158158\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.drawing_primitives\n'
import arcadeplus, os
arcadeplus.open_window(600, 600, 'Drawing Primitives Example')
arcadeplus.set_background_color(arcadeplus.color.WHITE)
arcadeplus.start_render()
for x in range(0, 601, 120):
    arcadeplus.draw_line(x, 0, x, 600, arcadeplus.color.BLACK, 2)

for y in range(0, 601, 200):
    arcadeplus.draw_line(0, y, 800, y, arcadeplus.color.BLACK, 2)

arcadeplus.draw_text('draw_point', 3, 405, arcadeplus.color.BLACK, 12)
arcadeplus.draw_point(60, 495, arcadeplus.color.RED, 10)
arcadeplus.draw_text('draw_points', 123, 405, arcadeplus.color.BLACK, 12)
point_list = ((165, 495), (165, 480), (165, 465), (195, 495), (195, 480), (195, 465))
arcadeplus.draw_points(point_list, arcadeplus.color.ZAFFRE, 10)
arcadeplus.draw_text('draw_line', 243, 405, arcadeplus.color.BLACK, 12)
arcadeplus.draw_line(270, 495, 300, 450, arcadeplus.color.WOOD_BROWN, 3)
arcadeplus.draw_text('draw_lines', 363, 405, arcadeplus.color.BLACK, 12)
point_list = ((390, 450), (450, 450), (390, 480), (450, 480), (390, 510), (450, 510))
arcadeplus.draw_lines(point_list, arcadeplus.color.BLUE, 3)
arcadeplus.draw_text('draw_line_strip', 483, 405, arcadeplus.color.BLACK, 12)
point_list = ((510, 450), (570, 450), (510, 480), (570, 480), (510, 510), (570, 510))
arcadeplus.draw_line_strip(point_list, arcadeplus.color.TROPICAL_RAIN_FOREST, 3)
arcadeplus.draw_text('draw_polygon_outline', 3, 207, arcadeplus.color.BLACK, 9)
point_list = ((30, 240), (45, 240), (60, 255), (60, 285), (45, 300), (30, 300))
arcadeplus.draw_polygon_outline(point_list, arcadeplus.color.SPANISH_VIOLET, 3)
arcadeplus.draw_text('draw_polygon_filled', 123, 207, arcadeplus.color.BLACK, 9)
point_list = ((150, 240), (165, 240), (180, 255), (180, 285), (165, 300), (150, 300))
arcadeplus.draw_polygon_filled(point_list, arcadeplus.color.SPANISH_VIOLET)
arcadeplus.draw_text('draw_circle_outline', 243, 207, arcadeplus.color.BLACK, 10)
arcadeplus.draw_circle_outline(300, 285, 18, arcadeplus.color.WISTERIA, 3)
arcadeplus.draw_text('draw_circle_filled', 363, 207, arcadeplus.color.BLACK, 10)
arcadeplus.draw_circle_filled(420, 285, 18, arcadeplus.color.GREEN)
arcadeplus.draw_text('draw_ellipse_outline', 483, 207, arcadeplus.color.BLACK, 10)
arcadeplus.draw_ellipse_outline(540, 273, 15, 36, arcadeplus.color.AMBER, 3)
arcadeplus.draw_ellipse_outline(540, 336, 15, 36, arcadeplus.color.BLACK_BEAN, 3, 45)
arcadeplus.draw_text('draw_ellipse_filled', 3, 3, arcadeplus.color.BLACK, 10)
arcadeplus.draw_ellipse_filled(60, 81, 15, 36, arcadeplus.color.AMBER)
arcadeplus.draw_ellipse_filled(60, 144, 15, 36, arcadeplus.color.BLACK_BEAN, 45)
arcadeplus.draw_text('draw_arc/filled_arc', 123, 3, arcadeplus.color.BLACK, 10)
arcadeplus.draw_arc_outline(150, 81, 15, 36, arcadeplus.color.BRIGHT_MAROON, 90, 360)
arcadeplus.draw_arc_filled(150, 144, 15, 36, arcadeplus.color.BOTTLE_GREEN, 90, 360, 45)
arcadeplus.draw_text('draw_rect', 243, 3, arcadeplus.color.BLACK, 10)
arcadeplus.draw_rectangle_outline(295, 100, 45, 65, arcadeplus.color.BRITISH_RACING_GREEN)
arcadeplus.draw_rectangle_outline(295, 160, 20, 45, arcadeplus.color.BRITISH_RACING_GREEN, 3, 45)
arcadeplus.draw_text('draw_filled_rect', 363, 3, arcadeplus.color.BLACK, 10)
arcadeplus.draw_rectangle_filled(420, 100, 45, 65, arcadeplus.color.BLUSH)
arcadeplus.draw_rectangle_filled(420, 160, 20, 40, arcadeplus.color.BLUSH, 45)
arcadeplus.draw_text('draw_bitmap', 483, 3, arcadeplus.color.BLACK, 12)
texture = arcadeplus.load_texture(':resources:images/space_shooter/playerShip1_orange.png')
scale = 0.6
arcadeplus.draw_scaled_texture_rectangle(540, 120, texture, scale, 0)
arcadeplus.draw_scaled_texture_rectangle(540, 60, texture, scale, 45)
arcadeplus.finish_render()
arcadeplus.run()