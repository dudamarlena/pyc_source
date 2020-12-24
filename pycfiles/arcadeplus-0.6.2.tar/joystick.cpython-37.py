# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\joystick.py
# Compiled at: 2020-03-29 18:05:46
# Size of source mod 2**32: 4364 bytes
__doc__ = '\nThis simple animation example shows how to move an item with the joystick.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.joystick\n'
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Joystick Control Example'
RECT_WIDTH = 50
RECT_HEIGHT = 50
MOVEMENT_MULTIPLIER = 5
DEAD_ZONE = 0.05

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player = None
        self.left_down = False
        joysticks = arcadeplus.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion
        else:
            print('There are no Joysticks')
            self.joystick = None

    def on_joybutton_press(self, _joystick, button):
        print('Button {} down'.format(button))

    def on_joybutton_release(self, _joystick, button):
        print('Button {} up'.format(button))

    def on_joyhat_motion(self, _joystick, hat_x, hat_y):
        print('Hat ({}, {})'.format(hat_x, hat_y))

    def setup(self):
        """ Set up the game and initialize the variables. """
        width = RECT_WIDTH
        height = RECT_HEIGHT
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        angle = 0
        color = arcadeplus.color.WHITE
        self.player = Rectangle(x, y, width, height, angle, color)
        self.left_down = False

    def on_update(self, dt):
        if self.joystick:
            self.player.delta_x = self.joystick.x * MOVEMENT_MULTIPLIER
            if abs(self.player.delta_x) < DEAD_ZONE:
                self.player.delta_x = 0
            self.player.delta_y = -self.joystick.y * MOVEMENT_MULTIPLIER
            if abs(self.player.delta_y) < DEAD_ZONE:
                self.player.delta_y = 0
        self.player.move()

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.player.draw()


class Rectangle:
    """Rectangle"""

    def __init__(self, x, y, width, height, angle, color):
        """ Initialize our rectangle variables """
        self.x = x
        self.y = y
        self.delta_x = 0
        self.delta_y = 0
        self.width = width
        self.height = height
        self.angle = angle
        self.color = color

    def draw(self):
        """ Draw our rectangle """
        arcadeplus.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color, self.angle)

    def move(self):
        """ Move our rectangle """
        self.x += self.delta_x
        if self.x < RECT_WIDTH // 2:
            self.x = RECT_WIDTH // 2
        if self.x > SCREEN_WIDTH - RECT_WIDTH // 2:
            self.x = SCREEN_WIDTH - RECT_WIDTH // 2
        self.y += self.delta_y
        if self.y < RECT_HEIGHT // 2:
            self.y = RECT_HEIGHT // 2
        if self.y > SCREEN_HEIGHT - RECT_HEIGHT // 2:
            self.y = SCREEN_HEIGHT - RECT_HEIGHT // 2


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()