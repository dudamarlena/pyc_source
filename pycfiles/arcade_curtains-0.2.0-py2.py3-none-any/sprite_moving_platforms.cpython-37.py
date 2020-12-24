# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_moving_platforms.py
# Compiled at: 2020-03-29 18:10:41
# Size of source mod 2**32: 8585 bytes
__doc__ = "\nSprite with Moving Platforms\n\nLoad a map stored in csv format, as exported by the program 'Tiled.'\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_moving_platforms\n"
import arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite with Moving Platforms Example'
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * SPRITE_SCALING
VIEWPORT_MARGIN = SPRITE_PIXEL_SIZE * SPRITE_SCALING
RIGHT_MARGIN = 4 * SPRITE_PIXEL_SIZE * SPRITE_SCALING
MOVEMENT_SPEED = 10 * SPRITE_SCALING
JUMP_SPEED = 28 * SPRITE_SCALING
GRAVITY = 0.9 * SPRITE_SCALING

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.all_sprites_list = None
        self.all_wall_list = None
        self.static_wall_list = None
        self.moving_wall_list = None
        self.player_list = None
        self.coin_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.game_over = False

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.all_wall_list = arcadeplus.SpriteList()
        self.static_wall_list = arcadeplus.SpriteList()
        self.moving_wall_list = arcadeplus.SpriteList()
        self.player_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 2 * GRID_PIXEL_SIZE
        self.player_sprite.center_y = 3 * GRID_PIXEL_SIZE
        self.player_list.append(self.player_sprite)
        for i in range(30):
            wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
            wall.bottom = 0
            wall.center_x = i * GRID_PIXEL_SIZE
            self.static_wall_list.append(wall)
            self.all_wall_list.append(wall)

        wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
        wall.center_y = 3 * GRID_PIXEL_SIZE
        wall.center_x = 3 * GRID_PIXEL_SIZE
        wall.boundary_left = 2 * GRID_PIXEL_SIZE
        wall.boundary_right = 5 * GRID_PIXEL_SIZE
        wall.change_x = 2 * SPRITE_SCALING
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)
        wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
        wall.center_y = 3 * GRID_PIXEL_SIZE
        wall.center_x = 7 * GRID_PIXEL_SIZE
        wall.boundary_left = 5 * GRID_PIXEL_SIZE
        wall.boundary_right = 9 * GRID_PIXEL_SIZE
        wall.change_x = -2 * SPRITE_SCALING
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)
        wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
        wall.center_y = 5 * GRID_PIXEL_SIZE
        wall.center_x = 5 * GRID_PIXEL_SIZE
        wall.boundary_top = 8 * GRID_PIXEL_SIZE
        wall.boundary_bottom = 4 * GRID_PIXEL_SIZE
        wall.change_y = 2 * SPRITE_SCALING
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)
        wall = arcadeplus.Sprite(':resources:images/tiles/grassMid.png', SPRITE_SCALING)
        wall.center_y = 5 * GRID_PIXEL_SIZE
        wall.center_x = 8 * GRID_PIXEL_SIZE
        wall.boundary_left = 7 * GRID_PIXEL_SIZE
        wall.boundary_right = 9 * GRID_PIXEL_SIZE
        wall.boundary_top = 8 * GRID_PIXEL_SIZE
        wall.boundary_bottom = 4 * GRID_PIXEL_SIZE
        wall.change_x = 2 * SPRITE_SCALING
        wall.change_y = 2 * SPRITE_SCALING
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)
        self.physics_engine = arcadeplus.PhysicsEnginePlatformer((self.player_sprite), (self.all_wall_list),
          gravity_constant=GRAVITY)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.view_left = 0
        self.view_bottom = 0
        self.game_over = False

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.static_wall_list.draw()
        self.moving_wall_list.draw()
        self.player_list.draw()
        distance = self.player_sprite.right
        output = f"Distance: {distance}"
        arcadeplus.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcadeplus.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcadeplus.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        changed = False
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True
        if changed:
            arcadeplus.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()