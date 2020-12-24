# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_bullets_enemy_aims.py
# Compiled at: 2020-03-29 18:09:05
# Size of source mod 2**32: 4847 bytes
__doc__ = '\nShow how to have enemies shoot bullets aimed at the player.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_bullets_enemy_aims\n'
import arcadeplus, math, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprites and Bullets Enemy Aims Example'
BULLET_SPEED = 4

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.frame_count = 0
        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
        self.player = None

    def setup(self):
        self.enemy_list = arcadeplus.SpriteList()
        self.bullet_list = arcadeplus.SpriteList()
        self.player_list = arcadeplus.SpriteList()
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
        self.frame_count += 1
        for enemy in self.enemy_list:
            start_x = enemy.center_x
            start_y = enemy.center_y
            dest_x = self.player.center_x
            dest_y = self.player.center_y
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)
            enemy.angle = math.degrees(angle) - 90
            if self.frame_count % 60 == 0:
                bullet = arcadeplus.Sprite(':resources:images/space_shooter/laserBlue01.png')
                bullet.center_x = start_x
                bullet.center_y = start_y
                bullet.angle = math.degrees(angle)
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED
                self.bullet_list.append(bullet)

        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = y


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()