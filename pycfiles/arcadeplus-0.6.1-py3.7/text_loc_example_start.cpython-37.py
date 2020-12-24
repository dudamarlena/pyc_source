# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\text_loc_example_start.py
# Compiled at: 2020-03-29 18:11:15
# Size of source mod 2**32: 1923 bytes
"""
Example showing how to draw text to the screen.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.text_loc_example_start
"""
import arcadeplus, os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = 'Localizing Text Example'

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.WHITE)
        self.text_angle = 0
        self.time_elapsed = 0.0

    def on_update(self, delta_time):
        self.text_angle += 1
        self.time_elapsed += delta_time

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        start_x = 50
        start_y = 450
        arcadeplus.draw_point(start_x, start_y, arcadeplus.color.BLUE, 5)
        arcadeplus.draw_text('Simple line of text in 12 point', start_x, start_y, arcadeplus.color.BLACK, 12)


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()