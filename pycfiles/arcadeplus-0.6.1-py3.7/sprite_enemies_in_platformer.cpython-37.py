# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_enemies_in_platformer.py
# Compiled at: 2020-03-29 18:09:56
# Size of source mod 2**32: 6655 bytes
"""
Show how to do enemies in a platformer

Artwork from: http://kenney.nl
Tiled available from: http://www.mapeditor.org/

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_enemies_in_platformer
"""
import arcadeplus, os
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Enemies in a Platformer Example'
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.5

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.wall_list = None
        self.enemy_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.wall_list = arcadeplus.SpriteList()
        self.enemy_list = arcadeplus.SpriteList()
        self.player_list = arcadeplus.SpriteList()
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        for x in range(SPRITE_SIZE * 3, SPRITE_SIZE * 8, SPRITE_SIZE):
            wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
            wall.bottom = SPRITE_SIZE * 3
            wall.left = x
            self.wall_list.append(wall)

        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE * 5):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.bottom = SPRITE_SIZE
            wall.left = x
            self.wall_list.append(wall)

        enemy = arcadeplus.Sprite(':resources:images/enemies/wormGreen.png', SPRITE_SCALING)
        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 2
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        enemy = arcadeplus.Sprite(':resources:images/enemies/wormGreen.png', SPRITE_SCALING)
        enemy.bottom = SPRITE_SIZE * 4
        enemy.left = SPRITE_SIZE * 4
        enemy.boundary_right = SPRITE_SIZE * 8
        enemy.boundary_left = SPRITE_SIZE * 3
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270
        self.physics_engine = arcadeplus.PhysicsEnginePlatformer((self.player_sprite), (self.wall_list),
          gravity_constant=GRAVITY)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcadeplus.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        else:
            if key == arcadeplus.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        if not self.game_over:
            self.enemy_list.update()
            for enemy in self.enemy_list:
                if len(arcadeplus.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                elif enemy.boundary_left is not None:
                    if enemy.left < enemy.boundary_left:
                        enemy.change_x *= -1
                if enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            self.physics_engine.update()
            if len(arcadeplus.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()