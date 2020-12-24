# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\snow.py
# Compiled at: 2020-03-29 18:08:41
# Size of source mod 2**32: 3265 bytes
__doc__ = '\nContributed to Python arcadeplus Library by Nicholas Hartunian\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.snow\n'
import random, math, arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Snow'

class Snowflake:
    """Snowflake"""

    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.snowflake_list = None

    def start_snowfall(self):
        """ Set up snowfall and initialize variables. """
        self.snowflake_list = []
        for i in range(50):
            snowflake = Snowflake()
            snowflake.x = random.randrange(SCREEN_WIDTH)
            snowflake.y = random.randrange(SCREEN_HEIGHT + 200)
            snowflake.size = random.randrange(4)
            snowflake.speed = random.randrange(20, 40)
            snowflake.angle = random.uniform(math.pi, math.pi * 2)
            self.snowflake_list.append(snowflake)

        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        for snowflake in self.snowflake_list:
            arcadeplus.draw_circle_filled(snowflake.x, snowflake.y, snowflake.size, arcadeplus.color.WHITE)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        for snowflake in self.snowflake_list:
            snowflake.y -= snowflake.speed * delta_time
            if snowflake.y < 0:
                snowflake.reset_pos()
            snowflake.x += snowflake.speed * math.cos(snowflake.angle) * delta_time
            snowflake.angle += 1 * delta_time


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.start_snowfall()
    arcadeplus.run()


if __name__ == '__main__':
    main()