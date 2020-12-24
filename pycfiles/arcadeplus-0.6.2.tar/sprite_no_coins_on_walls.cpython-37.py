# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_no_coins_on_walls.py
# Compiled at: 2020-03-29 18:10:45
# Size of source mod 2**32: 5434 bytes
__doc__ = "\nNo coins on the walls\n\nSimple program to show basic sprite usage. Specifically, create coin sprites that\naren't on top of any walls, and don't have coins on top of each other.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_no_coins_on_walls\n"
import arcadeplus, random, os
SPRITE_SCALING = 0.5
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite No Coins on Walls Example'
NUMBER_OF_COINS = 50
MOVEMENT_SPEED = 5

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.all_sprites_list = None
        self.coin_list = None
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.all_sprites_list = arcadeplus.SpriteList()
        self.wall_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        for y in range(0, 800, 200):
            for x in range(100, 700, 64):
                wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        for i in range(NUMBER_OF_COINS):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', SPRITE_SCALING_COIN)
            coin_placed_successfully = False
            while not coin_placed_successfully:
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)
                wall_hit_list = arcadeplus.check_for_collision_with_list(coin, self.wall_list)
                coin_hit_list = arcadeplus.check_for_collision_with_list(coin, self.coin_list)
                if len(wall_hit_list) == 0 and len(coin_hit_list) == 0:
                    coin_placed_successfully = True

            self.coin_list.append(coin)

        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_sprite.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()