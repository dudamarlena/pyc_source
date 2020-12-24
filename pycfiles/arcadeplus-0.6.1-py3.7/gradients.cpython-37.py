# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\gradients.py
# Compiled at: 2020-03-29 18:05:19
# Size of source mod 2**32: 3159 bytes
"""
Drawing Gradients

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.gradients
"""
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Gradients Example'

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.shapes = arcadeplus.ShapeElementList()
        color1 = (215, 214, 165)
        color2 = (219, 166, 123)
        points = ((0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT))
        colors = (color1, color1, color2, color2)
        rect = arcadeplus.create_rectangle_filled_with_colors(points, colors)
        self.shapes.append(rect)
        color1 = (165, 92, 85, 255)
        color2 = (165, 92, 85, 0)
        points = ((100, 100), (SCREEN_WIDTH - 100, 100), (SCREEN_WIDTH - 100, 300), (100, 300))
        colors = (color2, color1, color1, color2)
        rect = arcadeplus.create_rectangle_filled_with_colors(points, colors)
        self.shapes.append(rect)
        color1 = (7, 67, 88)
        color2 = (69, 137, 133)
        points = ((100, 400), (SCREEN_WIDTH - 100, 400), (SCREEN_WIDTH - 100, 500), (100, 500))
        colors = [color2, color1, color2, color1]
        shape = arcadeplus.create_lines_with_colors(points, colors, line_width=5)
        self.shapes.append(shape)
        color1 = (215, 214, 165)
        color2 = (219, 166, 123)
        color3 = (165, 92, 85)
        points = ((SCREEN_WIDTH // 2, 500), (SCREEN_WIDTH // 2 - 100, 400), (SCREEN_WIDTH // 2 + 100, 400))
        colors = (color1, color2, color3)
        shape = arcadeplus.create_triangles_filled_with_colors(points, colors)
        self.shapes.append(shape)
        color1 = (69, 137, 133, 127)
        color2 = (7, 67, 88, 127)
        shape = arcadeplus.create_ellipse_filled_with_colors((SCREEN_WIDTH // 2), 350, 50, 50, inside_color=color1,
          outside_color=color2)
        self.shapes.append(shape)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.shapes.draw()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()