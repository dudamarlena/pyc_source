# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\shape_list_demo_2.py
# Compiled at: 2020-03-29 18:07:36
# Size of source mod 2**32: 2297 bytes
__doc__ = "\nThis demo shows using buffered rectangles to draw a grid of squares on the\nscreen.\n\nFor me this starts at 0.500 seconds and goes down to 0.220 seconds after the\ngraphics card figures out some optimizations.\n\nIt is faster than demo 1 because we aren't loading the vertices and color\nto the card again and again. It isn't very fast because we are still sending\nindividual draw commands to the graphics card for each square.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.shape_list_demo_2\n"
import arcadeplus, timeit
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Shape List Demo 2'
SQUARE_WIDTH = 5
SQUARE_HEIGHT = 5
SQUARE_SPACING = 10

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.DARK_SLATE_GRAY)
        self.draw_time = 0
        self.shape_list = None

    def setup(self):
        self.shape_list = arcadeplus.ShapeElementList()
        for x in range(0, SCREEN_WIDTH, SQUARE_SPACING):
            for y in range(0, SCREEN_HEIGHT, SQUARE_SPACING):
                shape = arcadeplus.create_rectangle_filled(x, y, SQUARE_WIDTH, SQUARE_HEIGHT, arcadeplus.color.DARK_BLUE)
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