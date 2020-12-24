# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\text_loc_example_done.py
# Compiled at: 2020-03-29 18:11:12
# Size of source mod 2**32: 2097 bytes
__doc__ = '\nExample showing how to draw text to the screen.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.text_loc_example_done\n'
import arcadeplus, gettext, os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
gettext.install('text_loc_example', localedir='text_loc_example_locale')
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = 'Localizing Text Example'
_ = gettext.gettext

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.WHITE)
        self.text_angle = 0
        self.time_elapsed = 0.0

    def update(self, delta_time):
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
        arcadeplus.draw_text(_('Simple line of text in 12 point'), start_x, start_y, arcadeplus.color.BLACK, 12)


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()