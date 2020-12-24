# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\move_mouse.py
# Compiled at: 2020-03-29 18:06:13
# Size of source mod 2**32: 2400 bytes
__doc__ = '\nThis simple animation example shows how to move an item with the mouse, and\nhandle mouse clicks.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.move_mouse\n'
import arcadeplus
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = 'Move Mouse Example'

class Ball:

    def __init__(self, position_x, position_y, radius, color):
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcadeplus.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)


class MyGame(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.ASH_GREY)
        self.ball = Ball(50, 50, 15, arcadeplus.color.AUBURN)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcadeplus.start_render()
        self.ball.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.ball.position_x = x
        self.ball.position_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        print(f"You clicked button number: {button}")
        if button == arcadeplus.MOUSE_BUTTON_LEFT:
            self.ball.color = arcadeplus.color.BLACK

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        if button == arcadeplus.MOUSE_BUTTON_LEFT:
            self.ball.color = arcadeplus.color.AUBURN


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()