# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_move_walls.py
# Compiled at: 2020-03-29 18:10:38
# Size of source mod 2**32: 4202 bytes
"""
Sprite Move With Walls

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_move_walls
"""
import arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Move with Walls Example'
MOVEMENT_SPEED = 5

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.wall_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)
        for x in range(173, 650, 64):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 200
            self.wall_list.append(wall)

        for y in range(273, 500, 64):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.center_x = 465
            wall.center_y = y
            self.wall_list.append(wall)

        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        else:
            if key == arcadeplus.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            else:
                if key == arcadeplus.key.LEFT:
                    self.player_sprite.change_x = -MOVEMENT_SPEED
                else:
                    if key == arcadeplus.key.RIGHT:
                        self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = 0
        else:
            if key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
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