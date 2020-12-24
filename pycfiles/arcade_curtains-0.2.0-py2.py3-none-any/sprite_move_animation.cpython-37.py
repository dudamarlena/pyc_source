# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_move_animation.py
# Compiled at: 2020-03-29 18:10:18
# Size of source mod 2**32: 7719 bytes
__doc__ = '\nMove with a Sprite Animation\n\nSimple program to show basic sprite usage.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_move_animation\n'
import arcadeplus, random, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Move with a Sprite Animation Example'
COIN_SCALE = 0.5
COIN_COUNT = 50
CHARACTER_SCALING = 1
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7
RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
     arcadeplus.load_texture(filename),
     arcadeplus.load_texture(filename, mirrored=True)]


class PlayerCharacter(arcadeplus.Sprite):

    def __init__(self):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.scale = CHARACTER_SCALING
        self.points = [
         [
          -22, -64], [22, -64], [22, 28], [-22, 28]]
        main_path = ':resources:images/animated_characters/female_adventurer/femaleAdventurer'
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float=0.016666666666666666):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0:
            if self.character_face_direction == LEFT_FACING:
                self.character_face_direction = RIGHT_FACING
        if self.change_x == 0:
            if self.change_y == 0:
                self.texture = self.idle_texture_pair[self.character_face_direction]
                return
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[(self.cur_texture // UPDATES_PER_FRAME)][self.character_face_direction]


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.score = 0
        self.player = None

    def setup(self):
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.score = 0
        self.player = PlayerCharacter()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 0.8
        self.player_list.append(self.player)
        for i in range(COIN_COUNT):
            coin = arcadeplus.AnimatedTimeSprite(scale=0.5)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.textures = []
            coin.textures.append(arcadeplus.load_texture(':resources:images/items/gold_1.png'))
            coin.textures.append(arcadeplus.load_texture(':resources:images/items/gold_2.png'))
            coin.textures.append(arcadeplus.load_texture(':resources:images/items/gold_3.png'))
            coin.textures.append(arcadeplus.load_texture(':resources:images/items/gold_4.png'))
            coin.textures.append(arcadeplus.load_texture(':resources:images/items/gold_3.png'))
            coin.textures.append(arcadeplus.load_texture(':resources:images/items/gold_2.png'))
            coin.scale = COIN_SCALE
            coin.cur_texture_index = random.randrange(len(coin.textures))
            self.coin_list.append(coin)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcadeplus.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcadeplus.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.player.change_y = 0
        elif key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.coin_list.update()
        self.coin_list.update_animation()
        self.player_list.update()
        self.player_list.update_animation()
        hit_list = arcadeplus.check_for_collision_with_list(self.player, self.coin_list)
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()