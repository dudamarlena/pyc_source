# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_move_scrolling.py
# Compiled at: 2020-03-29 18:10:34
# Size of source mod 2**32: 6297 bytes
"""
Use sprites to scroll around a large screen.

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_move_scrolling
"""
import random, arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Move with Scrolling Screen Example'
VIEWPORT_MARGIN = 40
MOVEMENT_SPEED = 5

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.wall_list = arcadeplus.SpriteList()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', 0.4)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite)
        for x in range(200, 1650, 210):
            for y in range(0, 1000, 64):
                if random.randrange(5) > 0:
                    wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)

        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.view_left = 0
        self.view_bottom = 0

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
        changed = False
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
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
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)
        if changed:
            arcadeplus.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left - 1, self.view_bottom, SCREEN_HEIGHT + self.view_bottom - 1)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()