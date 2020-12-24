# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_bouncing_coins.py
# Compiled at: 2020-03-29 18:08:57
# Size of source mod 2**32: 4952 bytes
__doc__ = '\nSprite Simple Bouncing\n\nSimple program to show how to bounce items.\nThis only works for straight vertical and horizontal angles.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_bouncing_coins\n'
import arcadeplus, os, random
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 632
SCREEN_TITLE = 'Sprite Bouncing Coins'
MOVEMENT_SPEED = 5

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.coin_list = None
        self.wall_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.wall_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        for x in range(32, SCREEN_WIDTH, 64):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT - 32
            self.wall_list.append(wall)

        for y in range(96, SCREEN_HEIGHT, 64):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.center_x = 32
            wall.center_y = y
            self.wall_list.append(wall)
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.center_x = SCREEN_WIDTH - 32
            wall.center_y = y
            self.wall_list.append(wall)

        for x in range(128, SCREEN_WIDTH, 196):
            for y in range(128, SCREEN_HEIGHT, 196):
                wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        for i in range(10):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', 0.25)
            coin.center_x = random.randrange(100, 700)
            coin.center_y = random.randrange(100, 500)
            while coin.change_x == 0 and coin.change_y == 0:
                coin.change_x = random.randrange(-4, 5)
                coin.change_y = random.randrange(-4, 5)

            self.coin_list.append(coin)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.wall_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        for coin in self.coin_list:
            coin.center_x += coin.change_x
            walls_hit = arcadeplus.check_for_collision_with_list(coin, self.wall_list)
            for wall in walls_hit:
                if coin.change_x > 0:
                    coin.right = wall.left

            if len(walls_hit) > 0:
                coin.change_x *= -1
            coin.center_y += coin.change_y
            walls_hit = arcadeplus.check_for_collision_with_list(coin, self.wall_list)
            for wall in walls_hit:
                if coin.change_y > 0:
                    coin.top = wall.bottom

            if len(walls_hit) > 0:
                coin.change_y *= -1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()