# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_tiled_map_with_levels.py
# Compiled at: 2020-03-29 18:10:56
# Size of source mod 2**32: 8203 bytes
__doc__ = '\nLoad a Tiled map file with Levels\n\nArtwork from: http://kenney.nl\nTiled available from: http://www.mapeditor.org/\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_tiled_map_with_levels\n'
import arcadeplus, os, time
TILE_SPRITE_SCALING = 0.5
PLAYER_SCALING = 0.6
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Tiled Map with Levels Example'
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SPRITE_SCALING
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270
MOVEMENT_SPEED = 5
JUMP_SPEED = 23
GRAVITY = 1.1

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.wall_list = None
        self.player_list = None
        self.coin_list = None
        self.score = 0
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.game_over = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None
        self.level = 1
        self.max_level = 2

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', PLAYER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)
        self.load_level(self.level)
        self.game_over = False

    def load_level(self, level):
        my_map = arcadeplus.tilemap.read_tmx(f":resources:tmx_maps/level_{level}.tmx")
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE
        self.wall_list = arcadeplus.tilemap.process_layer(my_map, 'Platforms', TILE_SPRITE_SCALING)
        self.physics_engine = arcadeplus.PhysicsEnginePlatformer((self.player_sprite), (self.wall_list),
          gravity_constant=GRAVITY)
        if my_map.background_color:
            arcadeplus.set_background_color(my_map.background_color)
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """
        Render the screen.
        """
        self.frame_count += 1
        arcadeplus.start_render()
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        if self.last_time:
            if self.frame_count % 60 == 0:
                fps = 1.0 / (time.time() - self.last_time) * 60
                self.fps_message = f"FPS: {fps:5.0f}"
        if self.fps_message:
            arcadeplus.draw_text(self.fps_message, self.view_left + 10, self.view_bottom + 40, arcadeplus.color.BLACK, 14)
        if self.frame_count % 60 == 0:
            self.last_time = time.time()
        distance = self.player_sprite.right
        output = f"Distance: {distance:.0f}"
        arcadeplus.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcadeplus.color.BLACK, 14)
        if self.game_over:
            arcadeplus.draw_text('Game Over', self.view_left + 200, self.view_bottom + 200, arcadeplus.color.BLACK, 30)

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
        if self.player_sprite.right >= self.end_of_map:
            if self.level < self.max_level:
                self.level += 1
                self.load_level(self.level)
                self.player_sprite.center_x = 128
                self.player_sprite.center_y = 64
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
            else:
                self.game_over = True
        if not self.game_over:
            self.physics_engine.update()
        coins_hit = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

        changed = False
        left_bndry = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_TOP
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN_BOTTOM
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True
        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcadeplus.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()