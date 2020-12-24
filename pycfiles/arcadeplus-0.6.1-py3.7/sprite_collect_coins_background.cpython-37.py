# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_collect_coins_background.py
# Compiled at: 2020-03-29 18:09:25
# Size of source mod 2**32: 4579 bytes
"""
Sprite Collect Coins with Background

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_collect_coins_background
"""
import random, arcadeplus, os
PLAYER_SCALING = 0.5
COIN_SCALING = 0.25
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Collect Coins with Background Example'

class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.background = None
        self.player_list = None
        self.coin_list = None
        self.player_sprite = None
        self.score = 0
        self.score_text = None
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.background = arcadeplus.load_texture(':resources:images/backgrounds/abstract_1.jpg')
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', PLAYER_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        for i in range(50):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', COIN_SCALING)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        scale = SCREEN_WIDTH / self.background.width
        arcadeplus.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.coin_list.draw()
        self.player_list.draw()
        arcadeplus.draw_text(f"Score: {self.score}", 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.coin_list.update()
        hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()