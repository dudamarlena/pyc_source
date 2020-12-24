# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\timer.py
# Compiled at: 2020-03-29 18:11:22
# Size of source mod 2**32: 1590 bytes
"""
Show a timer on-screen.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.timer
"""
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Timer Example'

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

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