# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_move_keyboard_better.py
# Compiled at: 2020-03-29 18:10:28
# Size of source mod 2**32: 4734 bytes
"""
Better Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
This is slightly better than sprite_move_keyboard.py example
in how it works, but also slightly more complex.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_move_keyboard_better
"""
import arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Better Move Sprite with Keyboard Example'
MOVEMENT_SPEED = 5

class Player(arcadeplus.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        else:
            if self.right > SCREEN_WIDTH - 1:
                self.right = SCREEN_WIDTH - 1
            elif self.bottom < 0:
                self.bottom = 0
            else:
                if self.top > SCREEN_HEIGHT - 1:
                    self.top = SCREEN_HEIGHT - 1


class MyGame(arcadeplus.Window):
    __doc__ = '\n    Main application class.\n    '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.player_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.player_sprite = Player(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        if self.up_pressed:
            self.player_sprite.change_y = self.down_pressed or MOVEMENT_SPEED
        else:
            if self.down_pressed:
                if not self.up_pressed:
                    self.player_sprite.change_y = -MOVEMENT_SPEED
            elif self.left_pressed:
                self.player_sprite.change_x = self.right_pressed or -MOVEMENT_SPEED
            else:
                if self.right_pressed:
                    if not self.left_pressed:
                        self.player_sprite.change_x = MOVEMENT_SPEED
            self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.UP:
            self.up_pressed = True
        else:
            if key == arcadeplus.key.DOWN:
                self.down_pressed = True
            else:
                if key == arcadeplus.key.LEFT:
                    self.left_pressed = True
                else:
                    if key == arcadeplus.key.RIGHT:
                        self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcadeplus.key.UP:
            self.up_pressed = False
        else:
            if key == arcadeplus.key.DOWN:
                self.down_pressed = False
            else:
                if key == arcadeplus.key.LEFT:
                    self.left_pressed = False
                else:
                    if key == arcadeplus.key.RIGHT:
                        self.right_pressed = False


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()