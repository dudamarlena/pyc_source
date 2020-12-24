# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_bullets_random.py
# Compiled at: 2020-03-29 18:09:13
# Size of source mod 2**32: 3497 bytes
"""
Show how to have enemies shoot bullets at random intervals.

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_bullets_random
"""
import arcadeplus, random, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprites and Random Bullets Example'

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.frame_count = 0
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.player = None

    def setup(self):
        self.player_list = arcadeplus.SpriteList()
        self.enemy_list = arcadeplus.SpriteList()
        self.bullet_list = arcadeplus.SpriteList()
        self.player = arcadeplus.Sprite(':resources:images/space_shooter/playerShip1_orange.png', 0.5)
        self.player_list.append(self.player)
        enemy = arcadeplus.Sprite(':resources:images/space_shooter/playerShip1_green.png', 0.5)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)
        enemy = arcadeplus.Sprite(':resources:images/space_shooter/playerShip1_green.png', 0.5)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

    def on_draw(self):
        """Render the screen. """
        arcadeplus.start_render()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """
        for enemy in self.enemy_list:
            if random.randrange(200) == 0:
                bullet = arcadeplus.Sprite(':resources:images/space_shooter/laserBlue01.png')
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = -2
                self.bullet_list.append(bullet)

        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = 20


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()