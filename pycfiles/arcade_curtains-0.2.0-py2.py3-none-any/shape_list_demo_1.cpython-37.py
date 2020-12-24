# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\shape_list_demo_1.py
# Compiled at: 2020-03-29 18:07:33
# Size of source mod 2**32: 1785 bytes
__doc__ = '\nThis demo shows the speed of drawing a full grid of squares using no buffering.\n\nFor me this takes about 0.850 seconds per frame.\n\nIt is slow because we load all the points and all the colors to the card every\ntime.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.shape_list_demo_1\n'
import arcadeplus, timeit
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Shape List Demo 1'
SQUARE_WIDTH = 5
SQUARE_HEIGHT = 5
SQUARE_SPACING = 40

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.DARK_SLATE_GRAY)
        self.draw_time = 0

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        draw_start_time = timeit.default_timer()
        for x in range(0, SCREEN_WIDTH, SQUARE_SPACING):
            for y in range(0, SCREEN_HEIGHT, SQUARE_SPACING):
                arcadeplus.draw_rectangle_filled(x, y, SQUARE_WIDTH, SQUARE_HEIGHT, arcadeplus.color.DARK_BLUE)

        output = f"Drawing time: {self.draw_time:.3f} seconds per frame."
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 40, arcadeplus.color.WHITE, 18)
        self.draw_time = timeit.default_timer() - draw_start_time


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()