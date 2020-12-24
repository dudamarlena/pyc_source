# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_face_left_or_right.py
# Compiled at: 2020-03-29 18:10:06
# Size of source mod 2**32: 4608 bytes
"""
Sprite Facing Left or Right
Face left or right depending on our direction

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_face_left_or_right
"""
import arcadeplus, os
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite Face Left or Right Example'
MOVEMENT_SPEED = 5
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Player(arcadeplus.Sprite):

    def __init__(self):
        super().__init__()
        self.textures = []
        texture = arcadeplus.load_texture(':resources:images/enemies/bee.png')
        self.textures.append(texture)
        texture = arcadeplus.load_texture(':resources:images/enemies/bee.png', mirrored=True)
        self.textures.append(texture)
        self.scale = SPRITE_SCALING
        self.set_texture(TEXTURE_RIGHT)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        else:
            if self.change_x > 0:
                self.texture = self.textures[TEXTURE_RIGHT]
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
        self.all_sprites_list = None
        self.player_sprite = None
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.all_sprites_list = arcadeplus.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.all_sprites_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.all_sprites_list.update()

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


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()