# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\starting_template_simple.py
# Compiled at: 2020-03-29 18:11:03
# Size of source mod 2**32: 1216 bytes
"""
Starting Template Simple

Once you have learned how to use classes, you can begin your program with this
template.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.starting_template_simple
"""
import arcadeplus
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Starting Template Simple'

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()