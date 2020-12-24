# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\shape_list_non_center_rotate.py
# Compiled at: 2020-03-29 18:07:56
# Size of source mod 2**32: 1616 bytes
__doc__ = '\nShape List Non-center Rotation Demo\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.shape_list_non_center_rotate\n'
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Shape List Non-center Rotation Demo'

def make_shape():
    shape_list = arcadeplus.ShapeElementList()
    center_x = 20
    center_y = 30
    width = 30
    height = 40
    shape = arcadeplus.create_ellipse_filled(center_x, center_y, width, height, arcadeplus.color.WHITE)
    shape_list.append(shape)
    return shape_list


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = make_shape()
        self.shape_list.center_x = SCREEN_WIDTH / 2
        self.shape_list.center_y = SCREEN_HEIGHT / 2
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.shape_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.shape_list.angle += 1


def main():
    MyGame()
    arcadeplus.run()


if __name__ == '__main__':
    main()