# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_change_coins.py
# Compiled at: 2020-03-29 18:09:20
# Size of source mod 2**32: 4395 bytes
"""
Sprite Change Coins

This shows how you can change a sprite once it is hit, rather than eliminate it.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_change_coins
"""
import random, arcadeplus, os
SPRITE_SCALING = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Change Coins'

class Collectable(arcadeplus.Sprite):
    __doc__ = ' This class represents something the player collects. '

    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.changed = False


class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.a\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.score = 0
        self.player_sprite = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', 0.5)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        for i in range(50):
            coin = Collectable(':resources:images/items/coinGold.png', SPRITE_SCALING)
            coin.width = 30
            coin.height = 30
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_list.update()
        self.coin_list.update()
        hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list:
            if not coin.changed:
                coin.append_texture(arcadeplus.load_texture(':resources:images/pinball/bumper.png'))
                coin.set_texture(1)
                coin.changed = True
                coin.width = 30
                coin.height = 30
                self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()