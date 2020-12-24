# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sound_test.py
# Compiled at: 2020-03-29 18:08:53
# Size of source mod 2**32: 1804 bytes
__doc__ = ' Test for sound in arcadeplus.\n(May only work for windows at current time)\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sound_test\n'
import arcadeplus, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sound Test Example'
window = None

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        """Render the screen"""
        arcadeplus.start_render()
        text = 'Press left mouse to make noise'
        arcadeplus.draw_text(text, 150, 300, arcadeplus.color.WHITE, 30)

    def on_mouse_press(self, x, y, button, modifiers):
        """Plays sound on key press"""
        loaded_sound = arcadeplus.sound.load_sound(':resources:sounds/laser1.wav')
        arcadeplus.sound.play_sound(loaded_sound)

    def on_update(self, delta_time):
        """animations"""
        pass


def main():
    MyGame()
    arcadeplus.run()


if __name__ == '__main__':
    main()