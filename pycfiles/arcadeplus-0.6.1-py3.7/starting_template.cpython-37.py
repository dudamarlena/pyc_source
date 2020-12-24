# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\starting_template.py
# Compiled at: 2020-03-29 18:11:07
# Size of source mod 2**32: 2596 bytes
"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.starting_template
"""
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Starting Template'

class MyGame(arcadeplus.Window):
    __doc__ = "\n    Main application class.\n\n    NOTE: Go ahead and delete the methods you don't need.\n    If you do need a method, delete the 'pass' and replace it\n    with your own code. Don't leave 'pass' in this program.\n    "

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcadeplus.academy/arcadeplus.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()