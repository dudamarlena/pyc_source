# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\perlin_noise_2.py
# Compiled at: 2020-03-29 18:06:53
# Size of source mod 2**32: 4581 bytes
__doc__ = "\nPerlin Noise 2\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.perlin_noise_2\n\nTODO: This code doesn't work properly, and isn't currently listed in the examples.\n"
import arcadeplus, numpy as np
from PIL import Image
ROW_COUNT = 30
COLUMN_COUNT = 30
WIDTH = 10
HEIGHT = 10
MARGIN = 2
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = 'Perlin Noise 2 Example'

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
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background_list = None
        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.grid = None
        self.recreate_grid()

    def recreate_grid(self):
        lin = np.linspace(0, 5, ROW_COUNT, endpoint=False)
        y, x = np.meshgrid(lin, lin)
        self.grid = perlin(x, y, seed=0)
        self.grid *= 255
        self.grid += 128
        im = Image.fromarray(np.uint8(self.grid), 'L')
        background_sprite = arcadeplus.Sprite()
        background_sprite.center_x = SCREEN_WIDTH / 2
        background_sprite.center_y = SCREEN_HEIGHT / 2
        background_sprite.append_texture(arcadeplus.Texture('dynamic noise image', im))
        background_sprite.set_texture(0)
        self.background_list = arcadeplus.SpriteList()
        self.background_list.append(background_sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.background_list.draw()

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