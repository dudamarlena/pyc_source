# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\perlin_noise_1.py
# Compiled at: 2020-03-29 18:06:50
# Size of source mod 2**32: 4692 bytes
"""
Perlin Noise 1

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.perlin_noise_1

TODO: This code doesn't work properly, and isn't currently listed in the examples.
"""
import arcadeplus, numpy as np
from PIL import Image
ROW_COUNT = 30
COLUMN_COUNT = 30
WIDTH = 10
HEIGHT = 10
MARGIN = 2
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = 'Perlin Noise 1 Example'

def perlin(x, y, seed=0):
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    xi = x.astype(int)
    yi = y.astype(int)
    xf = x - xi
    yf = y - yi
    u = fade(xf)
    v = fade(yf)
    n00 = gradient(p[(p[xi] + yi)], xf, yf)
    n01 = gradient(p[(p[xi] + yi + 1)], xf, yf - 1)
    n11 = gradient(p[(p[(xi + 1)] + yi + 1)], xf - 1, yf - 1)
    n10 = gradient(p[(p[(xi + 1)] + yi)], xf - 1, yf)
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)


def lerp(a, b, x):
    """linear interpolation"""
    return a + x * (b - a)


def fade(t):
    """6t^5 - 15t^4 + 10t^3"""
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    """grad converts h to the right gradient vector and return the dot product with (x,y)"""
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[(h % 4)]
    return g[:, :, 0] * x + g[:, :, 1] * y


class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.shape_list = None
        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.grid = None
        self.recreate_grid()

    def recreate_grid(self):
        lin = np.linspace(0, 5, ROW_COUNT, endpoint=False)
        y, x = np.meshgrid(lin, lin)
        self.grid = perlin(x, y, seed=0)
        self.grid *= 255
        self.grid += 128
        self.shape_list = arcadeplus.ShapeElementList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                color = (
                 self.grid[row][column], 0, 0)
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                current_rect = arcadeplus.create_rectangle_filled(x, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)

        im = Image.fromarray(np.uint8(self.grid), 'L')
        im.save('test.png')

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
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)
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