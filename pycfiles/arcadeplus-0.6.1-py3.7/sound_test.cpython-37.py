# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sound_test.py
# Compiled at: 2020-03-29 18:08:53
# Size of source mod 2**32: 1804 bytes
""" Test for sound in arcadeplus.
(May only work for windows at current time)

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sound_test
"""
import arcadeplus, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sound Test Example'
window = None

class MyGame(arcadeplus.Window):
    __doc__ = ' Main sound test class '

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