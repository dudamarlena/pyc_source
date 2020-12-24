# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_collect_coins_move_down.py
# Compiled at: 2020-03-29 18:09:42
# Size of source mod 2**32: 4669 bytes
"""
Sprite Collect Coins Moving Down

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_collect_coins_move_down
"""
import random, arcadeplus, os
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Collect Coins Moving Down Example'

class Coin(arcadeplus.Sprite):
    __doc__ = '\n    This class represents the coins on our screen. It is a child class of\n    the arcadeplus library\'s "Sprite" class.\n    '

    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.reset_pos()


class MyGame(arcadeplus.Window):
    __doc__ = ' Our custom Window Class'

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_sprite_list = None
        self.coin_sprite_list = None
        self.player_sprite = None
        self.score = 0
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_sprite_list = arcadeplus.SpriteList()
        self.coin_sprite_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite_list.append(self.player_sprite)
        for i in range(COIN_COUNT):
            coin = Coin(':resources:images/items/coinGold.png', SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_sprite_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcadeplus.start_render()
        self.coin_sprite_list.draw()
        self.player_sprite_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.coin_sprite_list.update()
        hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_sprite_list)
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()