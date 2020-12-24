# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\timer.py
# Compiled at: 2020-03-29 18:11:22
# Size of source mod 2**32: 1590 bytes
__doc__ = '\nShow a timer on-screen.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.timer\n'
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Timer Example'

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.total_time = 0.0

    def setup(self):
        """
        Set up the application.
        """
        arcadeplus.set_background_color(arcadeplus.color.WHITE)
        self.total_time = 0.0

    def on_draw(self):
        """ Use this function to draw everything to the screen. """
        arcadeplus.start_render()
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcadeplus.draw_text(output, 300, 300, arcadeplus.color.BLACK, 30)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        self.total_time += delta_time


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()