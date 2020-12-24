# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\dual_stick_shooter.py
# Compiled at: 2020-03-29 18:05:05
# Size of source mod 2**32: 15553 bytes
"""
Dual-stick Shooter Example

A dual-analog stick joystick is the preferred method of input. If a joystick is
not present, the game will fail back to use keyboard controls (WASD to move, arrows to shoot)

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.dual_stick_shooter
"""
import arcadeplus, random, time, math, os
from typing import cast
import pprint, pyglet.input.base
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = 'Dual-stick Shooter Example'
MOVEMENT_SPEED = 4
BULLET_SPEED = 10
BULLET_COOLDOWN_TICKS = 10
ENEMY_SPAWN_INTERVAL = 1
ENEMY_SPEED = 1
JOY_DEADZONE = 0.2
ROTATE_OFFSET = -90

def dump_obj(obj):
    for key in sorted(vars(obj)):
        val = getattr(obj, key)
        print('{:30} = {} ({})'.format(key, val, type(val).__name__))


def dump_joystick(joy):
    print('========== {}'.format(joy))
    print('x       {}'.format(joy.x))
    print('y       {}'.format(joy.y))
    print('z       {}'.format(joy.z))
    print('rx      {}'.format(joy.rx))
    print('ry      {}'.format(joy.ry))
    print('rz      {}'.format(joy.rz))
    print('hat_x   {}'.format(joy.hat_x))
    print('hat_y   {}'.format(joy.hat_y))
    print('buttons {}'.format(joy.buttons))
    print('========== Extra joy')
    dump_obj(joy)
    print('========== Extra joy.device')
    dump_obj(joy.device)
    print('========== pprint joy')
    pprint.pprint(joy)
    print('========== pprint joy.device')
    pprint.pprint(joy.device)


def dump_joystick_state(ticks, joy):
    fmt_str = '{:6d} '
    num_fmts = ['{:5.2f}'] * 6
    fmt_str += ' '.join(num_fmts)
    fmt_str += ' {:2d} {:2d} {}'
    buttons = ' '.join(['{:5}'.format(str(b)) for b in joy.buttons])
    print(fmt_str.format(ticks, joy.x, joy.y, joy.z, joy.rx, joy.ry, joy.rz, joy.hat_x, joy.hat_y, buttons))


def get_joy_position--- This code section failed: ---

 L.  84         0  LOAD_FAST                'x'
                2  LOAD_GLOBAL              JOY_DEADZONE
                4  COMPARE_OP               >
                6  POP_JUMP_IF_TRUE     36  'to 36'
                8  LOAD_FAST                'x'
               10  LOAD_GLOBAL              JOY_DEADZONE
               12  UNARY_NEGATIVE   
               14  COMPARE_OP               <
               16  POP_JUMP_IF_TRUE     36  'to 36'
               18  LOAD_FAST                'y'
               20  LOAD_GLOBAL              JOY_DEADZONE
               22  COMPARE_OP               >
               24  POP_JUMP_IF_TRUE     36  'to 36'
               26  LOAD_FAST                'y'
               28  LOAD_GLOBAL              JOY_DEADZONE
               30  UNARY_NEGATIVE   
               32  COMPARE_OP               <
               34  POP_JUMP_IF_FALSE    74  'to 74'
             36_0  COME_FROM            24  '24'
             36_1  COME_FROM            16  '16'
             36_2  COME_FROM             6  '6'

 L.  85        36  LOAD_FAST                'y'
               38  UNARY_NEGATIVE   
               40  STORE_FAST               'y'

 L.  86        42  LOAD_GLOBAL              math
               44  LOAD_METHOD              atan2
               46  LOAD_FAST                'y'
               48  LOAD_FAST                'x'
               50  CALL_METHOD_2         2  '2 positional arguments'
               52  STORE_FAST               'rad'

 L.  87        54  LOAD_GLOBAL              math
               56  LOAD_METHOD              degrees
               58  LOAD_FAST                'rad'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  STORE_FAST               'angle'

 L.  88        64  LOAD_FAST                'x'
               66  LOAD_FAST                'y'
               68  LOAD_FAST                'angle'
               70  BUILD_TUPLE_3         3 
               72  RETURN_VALUE     
             74_0  COME_FROM            34  '34'

 L.  89        74  LOAD_CONST               (None, None, None)
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 76


class Player(arcadeplus.sprite.Sprite):

    def __init__(self, filename):
        super().__init__(filename=filename, scale=0.4, center_x=(SCREEN_WIDTH / 2), center_y=(SCREEN_HEIGHT / 2))
        self.shoot_up_pressed = False
        self.shoot_down_pressed = False
        self.shoot_left_pressed = False
        self.shoot_right_pressed = False


class Enemy(arcadeplus.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(filename=':resources:images/pinball/bumper.png', scale=0.5, center_x=x, center_y=y)

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of ENEMY_SPEED.
        """
        if self.center_y < player_sprite.center_y:
            self.center_y += min(ENEMY_SPEED, player_sprite.center_y - self.center_y)
        else:
            if self.center_y > player_sprite.center_y:
                self.center_y -= min(ENEMY_SPEED, self.center_y - player_sprite.center_y)
            elif self.center_x < player_sprite.center_x:
                self.center_x += min(ENEMY_SPEED, player_sprite.center_x - self.center_x)
            else:
                if self.center_x > player_sprite.center_x:
                    self.center_x -= min(ENEMY_SPEED, self.center_x - player_sprite.center_x)


class MyGame(arcadeplus.View):

    def __init__(self):
        super().__init__()
        self.game_over = False
        self.score = 0
        self.tick = 0
        self.bullet_cooldown = 0
        self.player = Player(':resources:images/space_shooter/playerShip2_orange.png')
        self.bullet_list = arcadeplus.SpriteList()
        self.enemy_list = arcadeplus.SpriteList()
        self.joy = None

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.DARK_MIDNIGHT_BLUE)
        joys = self.window.joys
        for joy in joys:
            dump_joystick(joy)

        if joys:
            self.joy = joys[0]
            print('Using joystick controls: {}'.format(self.joy.device))
            arcadeplus.window_commands.scheduleself.debug_joy_state0.1
        if not self.joy:
            print('No joystick present, using keyboard controls')
        arcadeplus.window_commands.scheduleself.spawn_enemyENEMY_SPAWN_INTERVAL

    def debug_joy_state(self, _delta_time):
        dump_joystick_state(self.tick, self.joy)

    def spawn_enemy(self, _elapsed):
        if self.game_over:
            return
        x = random.randint0SCREEN_WIDTH
        y = random.randint0SCREEN_HEIGHT
        self.enemy_list.append(Enemy(x, y))

    def on_update(self, delta_time):
        self.tick += 1
        if self.game_over:
            return
        self.bullet_cooldown += 1
        for enemy in self.enemy_list:
            cast(Enemy, enemy).follow_sprite(self.player)

        if self.joy:
            move_x, move_y, move_angle = get_joy_position(self.joy.move_stick_x, self.joy.move_stick_y)
            if move_angle:
                self.player.change_x = move_x * MOVEMENT_SPEED
                self.player.change_y = move_y * MOVEMENT_SPEED
                self.player.angle = move_angle + ROTATE_OFFSET
            else:
                self.player.change_x = 0
                self.player.change_y = 0
            shoot_x, shoot_y, shoot_angle = get_joy_position(self.joy.shoot_stick_x, self.joy.shoot_stick_y)
            if shoot_angle:
                self.spawn_bullet(shoot_angle)
        else:
            if self.player.shoot_right_pressed and self.player.shoot_up_pressed:
                self.spawn_bullet(45)
            else:
                if self.player.shoot_up_pressed and self.player.shoot_left_pressed:
                    self.spawn_bullet(135)
                else:
                    if self.player.shoot_left_pressed and self.player.shoot_down_pressed:
                        self.spawn_bullet(225)
                    else:
                        if self.player.shoot_down_pressed and self.player.shoot_right_pressed:
                            self.spawn_bullet(315)
                        else:
                            if self.player.shoot_right_pressed:
                                self.spawn_bullet(0)
                            else:
                                if self.player.shoot_up_pressed:
                                    self.spawn_bullet(90)
                                else:
                                    if self.player.shoot_left_pressed:
                                        self.spawn_bullet(180)
                                    else:
                                        if self.player.shoot_down_pressed:
                                            self.spawn_bullet(270)
                                        self.enemy_list.update()
                                        self.player.update()
                                        self.bullet_list.update()
                                        ship_death_hit_list = arcadeplus.check_for_collision_with_listself.playerself.enemy_list
                                        if len(ship_death_hit_list) > 0:
                                            self.game_over = True
                                        for bullet in self.bullet_list:
                                            bullet_killed = False
                                            enemy_shot_list = arcadeplus.check_for_collision_with_listbulletself.enemy_list
                                            for enemy in enemy_shot_list:
                                                enemy.remove_from_sprite_lists()
                                                bullet.remove_from_sprite_lists()
                                                bullet_killed = True
                                                self.score += 1

                                            if bullet_killed:
                                                continue

    def on_key_press(self, key, modifiers):
        if key == arcadeplus.key.W:
            self.player.change_y = MOVEMENT_SPEED
        else:
            if key == arcadeplus.key.A:
                self.player.change_x = -MOVEMENT_SPEED
            else:
                if key == arcadeplus.key.S:
                    self.player.change_y = -MOVEMENT_SPEED
                else:
                    if key == arcadeplus.key.D:
                        self.player.change_x = MOVEMENT_SPEED
                    else:
                        if key == arcadeplus.key.RIGHT:
                            self.player.shoot_right_pressed = True
                        else:
                            if key == arcadeplus.key.UP:
                                self.player.shoot_up_pressed = True
                            else:
                                if key == arcadeplus.key.LEFT:
                                    self.player.shoot_left_pressed = True
                                else:
                                    if key == arcadeplus.key.DOWN:
                                        self.player.shoot_down_pressed = True
        rad = math.atan2self.player.change_yself.player.change_x
        self.player.angle = math.degrees(rad) + ROTATE_OFFSET

    def on_key_release(self, key, modifiers):
        if key == arcadeplus.key.W:
            self.player.change_y = 0
        else:
            if key == arcadeplus.key.A:
                self.player.change_x = 0
            else:
                if key == arcadeplus.key.S:
                    self.player.change_y = 0
                else:
                    if key == arcadeplus.key.D:
                        self.player.change_x = 0
                    else:
                        if key == arcadeplus.key.RIGHT:
                            self.player.shoot_right_pressed = False
                        else:
                            if key == arcadeplus.key.UP:
                                self.player.shoot_up_pressed = False
                            else:
                                if key == arcadeplus.key.LEFT:
                                    self.player.shoot_left_pressed = False
                                else:
                                    if key == arcadeplus.key.DOWN:
                                        self.player.shoot_down_pressed = False
        rad = math.atan2self.player.change_yself.player.change_x
        self.player.angle = math.degrees(rad) + ROTATE_OFFSET

    def spawn_bullet(self, angle_in_deg):
        if self.bullet_cooldown < BULLET_COOLDOWN_TICKS:
            return
        self.bullet_cooldown = 0
        bullet = arcadeplus.Sprite':resources:images/space_shooter/laserBlue01.png'0.75
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        bullet.angle = angle_in_deg
        angle_in_rad = math.radians(angle_in_deg)
        bullet.change_x = math.cos(angle_in_rad) * BULLET_SPEED
        bullet.change_y = math.sin(angle_in_rad) * BULLET_SPEED
        self.bullet_list.append(bullet)

    def on_draw(self):
        arcadeplus.start_render()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.player.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 20, arcadeplus.color.WHITE, 14)
        if self.game_over:
            arcadeplus.draw_text('Game Over', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), (arcadeplus.color.WHITE), 100, width=SCREEN_WIDTH, align='center',
              anchor_x='center',
              anchor_y='center')


class JoyConfigView(arcadeplus.View):
    __doc__ = 'A View that allows a user to interactively configure their joystick'
    REGISTRATION_PAUSE = 1.5
    NO_JOYSTICK_PAUSE = 2.0
    JOY_ATTRS = ('x', 'y', 'z', 'rx', 'ry', 'rz')

    def __init__(self, joy_method_names, joysticks, next_view, width, height):
        super().__init__()
        self.next_view = next_view
        self.width = width
        self.height = height
        self.msg = ''
        self.script = self.joy_config_script()
        self.joys = joysticks
        arcadeplus.set_background_color(arcadeplus.color.WHITE)
        if len(joysticks) > 0:
            self.joy = joysticks[0]
            self.joy_method_names = joy_method_names
            self.axis_ranges = {}

    def config_axis(self, joy_axis_label, method_name):
        self.msg = joy_axis_label
        self.axis_ranges = {a:0.0 for a in self.JOY_ATTRS}
        while max([v for k, v in self.axis_ranges.items()]) < 0.85:
            for attr, farthest_val in self.axis_ranges.items():
                cur_val = getattr(self.joy, attr)
                if abs(cur_val) > abs(farthest_val):
                    self.axis_ranges[attr] = abs(cur_val)

            yield

        max_val = 0.0
        max_attr = None
        for attr, farthest_val in self.axis_ranges.items():
            if farthest_val > max_val:
                max_attr = attr
                max_val = farthest_val

        self.msg = 'Registered!'
        setattr(pyglet.input.base.Joystick, method_name, property(lambda that: getattr(that, max_attr), None))
        yield from self._pause(self.REGISTRATION_PAUSE)

    def joy_config_script(self):
        if len(self.joys) == 0:
            self.msg = 'No joysticks found!  Use keyboard controls.'
            yield from self._pause(self.NO_JOYSTICK_PAUSE)
            return
        for joy_axis_label, method_name in self.joy_method_names:
            yield from self.config_axisjoy_axis_labelmethod_name

        if False:
            yield None

    def on_update(self, delta_time):
        try:
            next(self.script)
        except StopIteration:
            self.window.show_view(self.next_view)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Configure your joystick', (self.width / 2), (self.height / 2 + 100), (arcadeplus.color.BLACK),
          font_size=32, anchor_x='center')
        arcadeplus.draw_text((self.msg), (self.width / 2), (self.height / 2), (arcadeplus.color.BLACK),
          font_size=24, anchor_x='center')

    def _pause(self, delay):
        """Block a generator from advancing for the given delay. Call with 'yield from self._pause(1.0)"""
        start = time.time()
        end = start + delay
        while time.time() < end:
            yield


if __name__ == '__main__':
    window = arcadeplus.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)
    window.joys = arcadeplus.get_joysticks()
    for j in window.joys:
        j.open()

    joy_config_method_names = (('Move the movement stick left or right', 'move_stick_x'),
                               ('Move the movement stick up or down', 'move_stick_y'),
                               ('Move the shooting stick left or right', 'shoot_stick_x'),
                               ('Move the shooting stick up or down', 'shoot_stick_y'))
    game = MyGame()
    window.show_view(JoyConfigView(joy_config_method_names, window.joys, game, SCREEN_WIDTH, SCREEN_HEIGHT))
    arcadeplus.run()