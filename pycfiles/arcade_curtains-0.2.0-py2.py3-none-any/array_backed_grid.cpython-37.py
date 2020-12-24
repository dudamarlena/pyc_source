# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\array_backed_grid.py
# Compiled at: 2020-03-29 18:04:09
# Size of source mod 2**32: 3461 bytes
__doc__ = '\nArray Backed Grid\n\nShow how to use a two-dimensional list/array to back the display of a\ngrid on-screen.\n\nNote: Regular drawing commands are slow. Particularly when drawing a lot of\nitems, like the rectangles in this example.\n\nFor faster drawing, create the shapes and then draw them as a batch.\nSee array_backed_grid_buffered.py\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.array_backed_grid\n'
import arcadeplus
ROW_COUNT = 15
COLUMN_COUNT = 15
WIDTH = 30
HEIGHT = 30
MARGIN = 5
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = 'Array Backed Grid Example'

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.grid = []
        for row in range(ROW_COUNT):
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)

        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == 1:
                    color = arcadeplus.color.GREEN
                else:
                    color = arcadeplus.color.WHITE
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                arcadeplus.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))
        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")
        if row < ROW_COUNT:
            if column < COLUMN_COUNT:
                if self.grid[row][column] == 0:
                    self.grid[row][column] = 1
                else:
                    self.grid[row][column] = 0


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()