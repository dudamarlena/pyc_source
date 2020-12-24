# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\resources.py
# Compiled at: 2020-03-29 18:07:30
# Size of source mod 2**32: 770 bytes
import arcadeplus
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Resources'

class MyGame(arcadeplus.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.sprite = arcadeplus.Sprite((arcadeplus.resources.image_male_adventurer_idle), center_x=50, center_y=50)
        self.sprite.velocity = (1, 1)

    def on_draw(self):
        arcadeplus.start_render()
        self.sprite.draw()

    def update(self, delta_time):
        self.sprite.update()


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()