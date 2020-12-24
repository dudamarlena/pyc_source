# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\array_backed_grid_buffered.py
# Compiled at: 2020-03-29 18:18:03
# Size of source mod 2**32: 3356 bytes
"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.array_backed_grid_buffered
"""
import arcadeplus
ROW_COUNT = 15
COLUMN_COUNT = 15
WIDTH = 30
HEIGHT = 30
MARGIN = 5
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = 'Array Backed Grid Buffered Example'

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.shape_list = None
        self.grid = []
        for row in range(ROW_COUNT):
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)

        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.recreate_grid()

    def recreate_grid(self):
        self.shape_list = arcadeplus.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == 0:
                    color = arcadeplus.color.WHITE
                else:
                    color = arcadeplus.color.GREEN
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                current_rect = arcadeplus.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.shape_list.draw()

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
        self.recreate_grid()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()