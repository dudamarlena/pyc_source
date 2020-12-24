# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\shape_list_demo_3.py
# Compiled at: 2020-03-29 18:07:39
# Size of source mod 2**32: 3322 bytes
"""
This demo shows drawing a grid of squares using a single buffer.

We calculate the points of each rectangle and add them to a point list.
We create a list of colors for each point.
We then draw all the squares with one drawing command.

This runs in about 0.000 seconds for me. It is much more complex in code
than the prior two examples, but the pay-off in speed is huge.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.shape_list_demo_3
"""
import arcadeplus, timeit
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Shape List Demo 3'
HALF_SQUARE_WIDTH = 2.5
HALF_SQUARE_HEIGHT = 2.5
SQUARE_SPACING = 10

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.DARK_SLATE_GRAY)
        self.draw_time = 0
        self.shape_list = None

    def setup(self):
        self.shape_list = arcadeplus.ShapeElementList()
        point_list = []
        color_list = []
        for x in range(0, SCREEN_WIDTH, SQUARE_SPACING):
            for y in range(0, SCREEN_HEIGHT, SQUARE_SPACING):
                top_left = (
                 x - HALF_SQUARE_WIDTH, y + HALF_SQUARE_HEIGHT)
                top_right = (x + HALF_SQUARE_WIDTH, y + HALF_SQUARE_HEIGHT)
                bottom_right = (x + HALF_SQUARE_WIDTH, y - HALF_SQUARE_HEIGHT)
                bottom_left = (x - HALF_SQUARE_WIDTH, y - HALF_SQUARE_HEIGHT)
                point_list.append(top_left)
                point_list.append(top_right)
                point_list.append(bottom_right)
                point_list.append(bottom_left)
                for i in range(4):
                    color_list.append(arcadeplus.color.DARK_BLUE)

        shape = arcadeplus.create_rectangles_filled_with_colors(point_list, color_list)
        self.shape_list.append(shape)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        draw_start_time = timeit.default_timer()
        self.shape_list.draw()
        output = f"Drawing time: {self.draw_time:.3f} seconds per frame."
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 40, arcadeplus.color.WHITE, 18)
        self.draw_time = timeit.default_timer() - draw_start_time


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()