# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_bullets_aimed.py
# Compiled at: 2020-03-29 18:09:00
# Size of source mod 2**32: 6104 bytes
"""
Sprite Bullets

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_bullets_aimed
"""
import random, arcadeplus, math, os
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprites and Bullets Aimed Example'
BULLET_SPEED = 5
window = None

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.coin_list = None
        self.bullet_list = None
        self.player_sprite = None
        self.score = 0
        self.score_text = None
        self.gun_sound = arcadeplus.sound.load_sound(':resources:sounds/laser1.wav')
        self.hit_sound = arcadeplus.sound.load_sound(':resources:sounds/phaseJump1.wav')
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.bullet_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)
        for i in range(COIN_COUNT):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)
            self.coin_list.append(coin)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse moves.
        """
        bullet = arcadeplus.Sprite(':resources:images/space_shooter/laserBlue01.png', SPRITE_SCALING_LASER)
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        dest_x = x
        dest_y = y
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED
        self.bullet_list.append(bullet)

    def on_update--- This code section failed: ---

 L. 157         0  LOAD_FAST                'self'
                2  LOAD_ATTR                bullet_list
                4  LOAD_METHOD              update
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  POP_TOP          

 L. 160        10  SETUP_LOOP          148  'to 148'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                bullet_list
               16  GET_ITER         
             18_0  COME_FROM           134  '134'
               18  FOR_ITER            146  'to 146'
               20  STORE_FAST               'bullet'

 L. 163        22  LOAD_GLOBAL              arcadeplus
               24  LOAD_METHOD              check_for_collision_with_list
               26  LOAD_FAST                'bullet'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                coin_list
               32  CALL_METHOD_2         2  '2 positional arguments'
               34  STORE_FAST               'hit_list'

 L. 166        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'hit_list'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  LOAD_CONST               0
               44  COMPARE_OP               >
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 167        48  LOAD_FAST                'bullet'
               50  LOAD_METHOD              remove_from_sprite_lists
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  POP_TOP          
             56_0  COME_FROM            46  '46'

 L. 170        56  SETUP_LOOP           92  'to 92'
               58  LOAD_FAST                'hit_list'
               60  GET_ITER         
               62  FOR_ITER             90  'to 90'
               64  STORE_FAST               'coin'

 L. 171        66  LOAD_FAST                'coin'
               68  LOAD_METHOD              remove_from_sprite_lists
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  POP_TOP          

 L. 172        74  LOAD_FAST                'self'
               76  DUP_TOP          
               78  LOAD_ATTR                score
               80  LOAD_CONST               1
               82  INPLACE_ADD      
               84  ROT_TWO          
               86  STORE_ATTR               score
               88  JUMP_BACK            62  'to 62'
               90  POP_BLOCK        
             92_0  COME_FROM_LOOP       56  '56'

 L. 175        92  LOAD_FAST                'bullet'
               94  LOAD_ATTR                bottom
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                width
              100  COMPARE_OP               >
              102  POP_JUMP_IF_TRUE    136  'to 136'
              104  LOAD_FAST                'bullet'
              106  LOAD_ATTR                top
              108  LOAD_CONST               0
              110  COMPARE_OP               <
              112  POP_JUMP_IF_TRUE    136  'to 136'
              114  LOAD_FAST                'bullet'
              116  LOAD_ATTR                right
              118  LOAD_CONST               0
              120  COMPARE_OP               <
              122  POP_JUMP_IF_TRUE    136  'to 136'
              124  LOAD_FAST                'bullet'
              126  LOAD_ATTR                left
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                width
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE    18  'to 18'
            136_0  COME_FROM           122  '122'
            136_1  COME_FROM           112  '112'
            136_2  COME_FROM           102  '102'

 L. 176       136  LOAD_FAST                'bullet'
              138  LOAD_METHOD              remove_from_sprite_lists
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  POP_TOP          
              144  JUMP_BACK            18  'to 18'
              146  POP_BLOCK        
            148_0  COME_FROM_LOOP       10  '10'

Parse error at or near `POP_BLOCK' instruction at offset 146


def main():
    game = MyGame()
    game.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()