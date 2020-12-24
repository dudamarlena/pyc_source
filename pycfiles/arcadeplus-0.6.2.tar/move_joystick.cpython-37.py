# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\move_joystick.py
# Compiled at: 2020-03-29 18:06:07
# Size of source mod 2**32: 3514 bytes
__doc__ = '\nThis simple animation example shows how to move an item with the joystick\nand game-pad.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.move_joystick\n'
import arcadeplus
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = 'Move Joystick Example'
MOVEMENT_SPEED = 5
DEAD_ZONE = 0.02

class Ball:

    def __init__(self, position_x, position_y, change_x, change_y, radius, color):
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcadeplus.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self):
        self.position_y += self.change_y
        self.position_x += self.change_x
        if self.position_x < self.radius:
            self.position_x = self.radius
        if self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius
        if self.position_y < self.radius:
            self.position_y = self.radius
        if self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius


class MyGame(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.ASH_GREY)
        self.ball = Ball(50, 50, 0, 0, 15, arcadeplus.color.AUBURN)
        joysticks = arcadeplus.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
        else:
            print('There are no joysticks.')
            self.joystick = None

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcadeplus.start_render()
        self.ball.draw()

    def on_update(self, delta_time):
        if self.joystick:
            if abs(self.joystick.x) < DEAD_ZONE:
                self.ball.change_x = 0
            else:
                self.ball.change_x = self.joystick.x * MOVEMENT_SPEED
            if abs(self.joystick.y) < DEAD_ZONE:
                self.ball.change_y = 0
            else:
                self.ball.change_y = -self.joystick.y * MOVEMENT_SPEED
        self.ball.update()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()