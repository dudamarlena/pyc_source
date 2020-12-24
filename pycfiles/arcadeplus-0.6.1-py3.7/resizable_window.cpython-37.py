# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\resizable_window.py
# Compiled at: 2020-03-29 18:07:26
# Size of source mod 2**32: 1798 bytes
"""
Example showing how handle screen resizing.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.resizable_window
"""
import arcadeplus
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = 'Resizing Window Example'
START = 0
END = 2000
STEP = 50

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        print(f"Window resized to: {width}, {height}")

    def on_draw(self):
        """ Render the screen. """
        arcadeplus.start_render()
        i = 0
        for y in range(START, END, STEP):
            arcadeplus.draw_point(0, y, arcadeplus.color.BLUE, 5)
            arcadeplus.draw_text((f"{y}"), 5, y, (arcadeplus.color.BLACK), 12, anchor_x='left', anchor_y='bottom')
            i += 1

        i = 1
        for x in range(START + STEP, END, STEP):
            arcadeplus.draw_point(x, 0, arcadeplus.color.BLUE, 5)
            arcadeplus.draw_text((f"{x}"), x, 5, (arcadeplus.color.BLACK), 12, anchor_x='left', anchor_y='bottom')
            i += 1


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()