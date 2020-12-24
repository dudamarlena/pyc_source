# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_collect_coins_move_circle.py
# Compiled at: 2020-03-29 18:22:39
# Size of source mod 2**32: 5119 bytes
__doc__ = '\nSprite Collect Coins Moving in Circles\n\nSimple program to show basic sprite usage.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_collect_coins_move_circle\n'
import random, arcadeplus, math, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Collect Coins Moving in Circles Example'

class Coin(arcadeplus.Sprite):

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.circle_angle = 0
        self.circle_radius = 0
        self.circle_speed = 0.008
        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):
        """ Update the ball's position. """
        self.center_x = self.circle_radius * math.sin(self.circle_angle) + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) + self.circle_center_y
        self.circle_angle += self.circle_speed


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.all_sprites_list = None
        self.coin_list = None
        self.score = 0
        self.player_sprite = None

    def start_new_game(self):
        """ Set up the game and initialize the variables. """
        self.all_sprites_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.all_sprites_list.append(self.player_sprite)
        for i in range(50):
            coin = Coin(':resources:images/items/coinGold.png', SPRITE_SCALING / 3)
            coin.circle_center_x = random.randrange(SCREEN_WIDTH)
            coin.circle_center_y = random.randrange(SCREEN_HEIGHT)
            coin.circle_radius = random.randrange(10, 200)
            coin.circle_angle = random.random() * 2 * math.pi
            self.all_sprites_list.append(coin)
            self.coin_list.append(coin)

        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        arcadeplus.start_render()
        self.all_sprites_list.draw()
        output = 'Score: ' + str(self.score)
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.all_sprites_list.update()
        hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list:
            self.score += 1
            coin.remove_from_sprite_lists()


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.start_new_game()
    arcadeplus.run()


if __name__ == '__main__':
    main()