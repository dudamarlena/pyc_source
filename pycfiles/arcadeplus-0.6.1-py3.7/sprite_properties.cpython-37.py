# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_properties.py
# Compiled at: 2020-03-29 18:10:48
# Size of source mod 2**32: 4875 bytes
"""
Sprites with Properties Example

Simple program to show how to store properties on sprites.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_properties

"""
import arcadeplus, os
SPRITE_SCALING_PLAYER = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprites with Properties Example'

class MyGame(arcadeplus.Window):
    __doc__ = ' Our custom Window Class'

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.player_sprite = None
        self.trigger_sprite = None
        self.set_mouse_visible(False)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)
        for x in range(100, 800, 100):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', scale=0.3, center_x=x, center_y=400)
            coin.intensity = 'dim'
            coin.alpha = 64
            self.coin_list.append(coin)

        self.trigger_sprite = arcadeplus.Sprite(':resources:images/pinball/bumper.png', scale=0.5, center_x=750, center_y=50)

    def on_draw(self):
        """ Draw everything """
        arcadeplus.start_render()
        self.coin_list.draw()
        self.trigger_sprite.draw()
        self.player_list.draw()
        instructions1 = "Touch a coin to set its intensity property to 'bright'."
        arcadeplus.draw_text(instructions1, 10, 90, arcadeplus.color.WHITE, 14)
        instructions2 = "Touch the trigger at the bottom-right to destroy all 'bright' sprites."
        arcadeplus.draw_text(instructions2, 10, 70, arcadeplus.color.WHITE, 14)
        coins_are_bright = [coin.intensity == 'bright' for coin in self.coin_list]
        output_any = f"Any sprites have intensity=bright? : {any(coins_are_bright)}"
        arcadeplus.draw_text(output_any, 10, 40, arcadeplus.color.WHITE, 14)
        output_all = f"All sprites have intensity=bright? : {all(coins_are_bright)}"
        arcadeplus.draw_text(output_all, 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.coin_list.update()
        coins_hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_hit_list:
            coin.intensity = 'bright'
            coin.alpha = 255

        hit_trigger = arcadeplus.check_for_collision(self.player_sprite, self.trigger_sprite)
        if hit_trigger:
            intense_sprites = [sprite for sprite in self.coin_list if sprite.intensity == 'bright']
            for coin in intense_sprites:
                coin.remove_from_sprite_lists()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()