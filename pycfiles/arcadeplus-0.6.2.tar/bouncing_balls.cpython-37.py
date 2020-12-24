# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\bouncing_balls.py
# Compiled at: 2020-03-29 18:04:21
# Size of source mod 2**32: 2885 bytes
__doc__ = '\nBounce balls on the screen.\nSpawn a new ball for each mouse-click.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.bouncing_balls\n'
import arcadeplus, random
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Bouncing Balls Example'

class Ball:
    """Ball"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.size = 0
        self.color = None


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    ball.size = random.randrange(10, 30)
    ball.x = random.randrange(ball.size, SCREEN_WIDTH - ball.size)
    ball.y = random.randrange(ball.size, SCREEN_HEIGHT - ball.size)
    ball.change_x = random.randrange(-2, 3)
    ball.change_y = random.randrange(-2, 3)
    ball.color = (
     random.randrange(256), random.randrange(256), random.randrange(256))
    return ball


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.ball_list = []
        ball = make_ball()
        self.ball_list.append(ball)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        for ball in self.ball_list:
            arcadeplus.draw_circle_filled(ball.x, ball.y, ball.size, ball.color)

        output = 'Balls: {}'.format(len(self.ball_list))
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """
        for ball in self.ball_list:
            ball.x += ball.change_x
            ball.y += ball.change_y
            if ball.x < ball.size:
                ball.change_x *= -1
            if ball.y < ball.size:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - ball.size:
                ball.change_x *= -1
            if ball.y > SCREEN_HEIGHT - ball.size:
                ball.change_y *= -1

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        ball = make_ball()
        self.ball_list.append(ball)


def main():
    MyGame()
    arcadeplus.run()


if __name__ == '__main__':
    main()