# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_bullets.py
# Compiled at: 2020-03-29 18:09:17
# Size of source mod 2**32: 5419 bytes
__doc__ = '\nSprite Bullets\n\nSimple program to show basic sprite usage.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_bullets\n'
import random, arcadeplus, os
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprites and Bullets Example'
BULLET_SPEED = 5

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.bullet_list = None
        self.player_sprite = None
        self.score = 0
        self.set_mouse_visible(False)
        self.gun_sound = arcadeplus.load_sound(':resources:sounds/hurt5.wav')
        self.hit_sound = arcadeplus.load_sound(':resources:sounds/hit5.wav')
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.bullet_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)
        for i in range(COIN_COUNT):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)
            self.coin_list.append(coin)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        arcadeplus.draw_text(f"Score: {self.score}", 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        arcadeplus.play_sound(self.gun_sound)
        bullet = arcadeplus.Sprite(':resources:images/space_shooter/laserBlue01.png', SPRITE_SCALING_LASER)
        bullet.angle = 90
        bullet.change_y = BULLET_SPEED
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.bullet_list.update()
        for bullet in self.bullet_list:
            hit_list = arcadeplus.check_for_collision_with_list(bullet, self.coin_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1
                arcadeplus.play_sound(self.hit_sound)

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()