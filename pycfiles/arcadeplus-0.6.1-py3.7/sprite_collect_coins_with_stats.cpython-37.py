# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_collect_coins_with_stats.py
# Compiled at: 2020-03-29 18:09:45
# Size of source mod 2**32: 5079 bytes
"""
Sprite Collect Coins with Stats

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_collect_coins_with_stats
"""
import random, arcadeplus, os, timeit
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Collect Coins with Stats Example'

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
        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None
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
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        draw_start_time = timeit.default_timer()
        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1
        arcadeplus.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)
        output = f"Processing time: {self.processing_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 20, arcadeplus.color.BLACK, 16)
        output = f"Drawing time: {self.draw_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 40, arcadeplus.color.BLACK, 16)
        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 60, arcadeplus.color.BLACK, 16)
        self.draw_time = timeit.default_timer() - draw_start_time

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.coin_list.update()
        coins_hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()