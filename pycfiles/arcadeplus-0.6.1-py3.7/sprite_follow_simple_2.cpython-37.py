# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_follow_simple_2.py
# Compiled at: 2020-03-29 18:10:09
# Size of source mod 2**32: 5627 bytes
"""
Sprite Follow Player 2

This calculates a 'vector' towards the player and randomly updates it based
on the player's location. This is a bit more complex, but more interesting
way of following the player.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_follow_simple_2
"""
import random, arcadeplus, math, os
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 5
COIN_SPEED = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Follow Player Simple Example 2'
SPRITE_SPEED = 0.5

class Coin(arcadeplus.Sprite):
    __doc__ = '\n    This class represents the coins on our screen. It is a child class of\n    the arcadeplus library\'s "Sprite" class.\n    '

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """
        self.center_x += self.change_x
        self.center_y += self.change_y
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(angle) * COIN_SPEED
            self.change_y = math.sin(angle) * COIN_SPEED


class MyGame(arcadeplus.Window):
    __doc__ = ' Our custom Window Class'

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.player_sprite = None
        self.score = 0
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        for i in range(COIN_COUNT):
            coin = Coin(':resources:images/items/coinGold.png', SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcadeplus.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        for coin in self.coin_list:
            coin.follow_sprite(self.player_sprite)

        hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list:
            coin.kill()
            self.score += 1


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()