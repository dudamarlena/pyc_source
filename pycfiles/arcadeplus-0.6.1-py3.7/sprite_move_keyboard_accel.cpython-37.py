# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_move_keyboard_accel.py
# Compiled at: 2020-03-29 18:10:24
# Size of source mod 2**32: 6128 bytes
"""
Show how to use acceleration and friction

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_move_keyboard_accel
"""
import arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Better Move Sprite with Keyboard Example'
MAX_SPEED = 3.0
ACCELERATION_RATE = 0.1
FRICTION = 0.02

class Player(arcadeplus.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
            self.change_x = 0
        else:
            if self.right > SCREEN_WIDTH - 1:
                self.right = SCREEN_WIDTH - 1
                self.change_x = 0
            elif self.bottom < 0:
                self.bottom = 0
                self.change_y = 0
            else:
                if self.top > SCREEN_HEIGHT - 1:
                    self.top = SCREEN_HEIGHT - 1
                    self.change_y = 0


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
        arcadeplus.draw_text(f"X Speed: {self.player_sprite.change_x:6.3f}", 10, 50, arcadeplus.color.BLACK)
        arcadeplus.draw_text(f"Y Speed: {self.player_sprite.change_y:6.3f}", 10, 70, arcadeplus.color.BLACK)

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.player_sprite.change_x > FRICTION:
            self.player_sprite.change_x -= FRICTION
        else:
            if self.player_sprite.change_x < -FRICTION:
                self.player_sprite.change_x += FRICTION
            else:
                self.player_sprite.change_x = 0
        if self.player_sprite.change_y > FRICTION:
            self.player_sprite.change_y -= FRICTION
        else:
            if self.player_sprite.change_y < -FRICTION:
                self.player_sprite.change_y += FRICTION
            else:
                self.player_sprite.change_y = 0
        if self.up_pressed:
            self.down_pressed or self.player_sprite.change_y += ACCELERATION_RATE
        else:
            if self.down_pressed:
                if not self.up_pressed:
                    self.player_sprite.change_y += -ACCELERATION_RATE
        if self.left_pressed:
            self.right_pressed or self.player_sprite.change_x += -ACCELERATION_RATE
        else:
            if self.right_pressed:
                if not self.left_pressed:
                    self.player_sprite.change_x += ACCELERATION_RATE
                if self.player_sprite.change_x > MAX_SPEED:
                    self.player_sprite.change_x = MAX_SPEED
            elif self.player_sprite.change_x < -MAX_SPEED:
                self.player_sprite.change_x = -MAX_SPEED
        if self.player_sprite.change_y > MAX_SPEED:
            self.player_sprite.change_y = MAX_SPEED
        else:
            if self.player_sprite.change_y < -MAX_SPEED:
                self.player_sprite.change_y = -MAX_SPEED
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