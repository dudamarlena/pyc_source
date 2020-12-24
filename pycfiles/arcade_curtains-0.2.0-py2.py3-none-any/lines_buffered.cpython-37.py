# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\lines_buffered.py
# Compiled at: 2020-03-29 18:05:50
# Size of source mod 2**32: 2270 bytes
__doc__ = '\nUsing a Vertex Buffer Object With Lines\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.lines_buffered\n'
import arcadeplus, random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Vertex Buffer Object With Lines Example'

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.shape_list = arcadeplus.ShapeElementList()
        point_list = ((0, 50), (10, 10), (50, 0), (10, -10), (0, -50), (-10, -10),
                      (-50, 0), (-10, 10), (0, 50))
        colors = [getattr(arcadeplus.color, color) for color in dir(arcadeplus.color) if not color.startswith('__')]
        for i in range(200):
            x = SCREEN_WIDTH // 2 - random.randrange(SCREEN_WIDTH)
            y = SCREEN_HEIGHT // 2 - random.randrange(SCREEN_HEIGHT)
            color = random.choice(colors)
            points = [(px + x, py + y) for px, py in point_list]
            my_line_strip = arcadeplus.create_line_strip(points, color, 5)
            self.shape_list.append(my_line_strip)

        self.shape_list.center_x = SCREEN_WIDTH // 2
        self.shape_list.center_y = SCREEN_HEIGHT // 2
        self.shape_list.angle = 0
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.shape_list.draw()

    def on_update(self, delta_time):
        self.shape_list.angle += 1
        self.shape_list.center_x += 0.1
        self.shape_list.center_y += 0.1


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()