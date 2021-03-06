# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_collect_coins_diff_levels.py
# Compiled at: 2020-03-29 18:09:29
# Size of source mod 2**32: 5946 bytes
__doc__ = '\nSprite Collect Coins with Different Levels\n\nSimple program to show basic sprite usage.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_collect_coins_diff_levels\n'
import random, arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Collect Coins with Different Levels Example'

class FallingCoin(arcadeplus.Sprite):
    """FallingCoin"""

    def update(self):
        """ Move the coin """
        self.center_y -= 2
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT


class RisingCoin(arcadeplus.Sprite):
    """RisingCoin"""

    def update(self):
        """ Move the coin """
        self.center_y += 2
        if self.bottom > SCREEN_HEIGHT:
            self.top = 0


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.player_sprite = None
        self.score = 0
        self.level = 1
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def level_1(self):
        for i in range(20):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', SPRITE_SCALING / 3)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def level_2(self):
        for i in range(30):
            coin = FallingCoin('images/gold_1.png', SPRITE_SCALING / 2)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
            self.coin_list.append(coin)

    def level_3(self):
        for i in range(30):
            coin = RisingCoin('images/gold_1.png', SPRITE_SCALING / 2)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(-SCREEN_HEIGHT, 0)
            self.coin_list.append(coin)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.score = 0
        self.level = 1
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.level_1()

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.player_sprite.draw()
        self.coin_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 15)
        output = f"Level: {self.level}"
        arcadeplus.draw_text(output, 10, 35, arcadeplus.color.WHITE, 15)

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

        if len(self.coin_list) == 0 and self.level == 1:
            self.level += 1
            self.level_2()
        elif len(self.coin_list) == 0:
            if self.level == 2:
                self.level += 1
                self.level_3()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()