# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_move_angle.py
# Compiled at: 2020-03-29 18:10:15
# Size of source mod 2**32: 4084 bytes
__doc__ = '\nMove Sprite by Angle\n\nSimple program to show basic sprite usage.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_move_angle\n'
import arcadeplus, os, math
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Move Sprite by Angle Example'
MOVEMENT_SPEED = 5
ANGLE_SPEED = 5

class Player(arcadeplus.Sprite):
    """Player"""

    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.speed = 0

    def update(self):
        angle_rad = math.radians(self.angle)
        self.angle += self.change_angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.player_sprite = None
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.player_sprite = Player(':resources:images/space_shooter/playerShip1_orange.png', SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.UP:
            self.player_sprite.speed = MOVEMENT_SPEED
        elif key == arcadeplus.key.DOWN:
            self.player_sprite.speed = -MOVEMENT_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.player_sprite.change_angle = -ANGLE_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.player_sprite.speed = 0
        elif key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player_sprite.change_angle = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()