# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\slime_invaders.py
# Compiled at: 2020-03-29 18:08:25
# Size of source mod 2**32: 12857 bytes
__doc__ = "\nSlime Invaders\n\nArtwork from http://kenney.nl\n\nThis example shows how to:\n\n* Get sprites to move as a group\n* Change texture of sprites as a group\n* Only have the bottom sprite in the group fire lasers\n* Create 'shields' like in space invaders\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.slime_invaders\n"
import random, arcadeplus
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_enemy = 0.5
SPRITE_SCALING_LASER = 0.8
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Slime Invaders'
BULLET_SPEED = 5
ENEMY_SPEED = 2
MAX_PLAYER_BULLETS = 3
ENEMY_VERTICAL_MARGIN = 15
RIGHT_ENEMY_BORDER = SCREEN_WIDTH - ENEMY_VERTICAL_MARGIN
LEFT_ENEMY_BORDER = ENEMY_VERTICAL_MARGIN
ENEMY_MOVE_DOWN_AMOUNT = 30
GAME_OVER = 1
PLAY_GAME = 0

class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.shield_list = None
        self.enemy_textures = None
        self.game_state = PLAY_GAME
        self.player_sprite = None
        self.score = 0
        self.enemy_change_x = -ENEMY_SPEED
        self.set_mouse_visible(False)
        self.gun_sound = arcadeplus.load_sound(':resources:sounds/hurt5.wav')
        self.hit_sound = arcadeplus.load_sound(':resources:sounds/hit5.wav')
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def setup_level_one(self):
        self.enemy_textures = []
        texture = arcadeplus.load_texture(':resources:images/enemies/slimeBlue.png', mirrored=True)
        self.enemy_textures.append(texture)
        texture = arcadeplus.load_texture(':resources:images/enemies/slimeBlue.png')
        self.enemy_textures.append(texture)
        x_count = 7
        x_start = 380
        x_spacing = 60
        y_count = 5
        y_start = 420
        y_spacing = 40
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
                enemy = arcadeplus.Sprite()
                enemy.scale = SPRITE_SCALING_enemy
                enemy.texture = self.enemy_textures[1]
                enemy.center_x = x
                enemy.center_y = y
                self.enemy_list.append(enemy)

    def make_shield(self, x_start):
        """
        Make a shield, which is just a 2D grid of solid color sprites
        stuck together with no margin so you can't tell them apart.
        """
        shield_block_width = 5
        shield_block_height = 10
        shield_width_count = 20
        shield_height_count = 5
        y_start = 150
        for x in range(x_start, x_start + shield_width_count * shield_block_width, shield_block_width):
            for y in range(y_start, y_start + shield_height_count * shield_block_height, shield_block_height):
                shield_sprite = arcadeplus.SpriteSolidColor(shield_block_width, shield_block_height, arcadeplus.color.WHITE)
                shield_sprite.center_x = x
                shield_sprite.center_y = y
                self.shield_list.append(shield_sprite)

    def setup(self):
        """
        Set up the game and initialize the variables.
        Call this method if you implement a 'play again' feature.
        """
        self.game_state = PLAY_GAME
        self.player_list = arcadeplus.SpriteList()
        self.enemy_list = arcadeplus.SpriteList()
        self.player_bullet_list = arcadeplus.SpriteList()
        self.enemy_bullet_list = arcadeplus.SpriteList()
        self.shield_list = arcadeplus.SpriteList(is_static=True)
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)
        for x in range(75, 800, 190):
            self.make_shield(x)

        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.setup_level_one()

    def on_draw(self):
        """ Render the screen. """
        arcadeplus.start_render()
        self.enemy_list.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.shield_list.draw()
        self.player_list.draw()
        arcadeplus.draw_text(f"Score: {self.score}", 10, 20, arcadeplus.color.WHITE, 14)
        if self.game_state == GAME_OVER:
            arcadeplus.draw_text('GAME OVER', 250, 300, arcadeplus.color.WHITE, 55)
            self.set_mouse_visible(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        if self.game_state == GAME_OVER:
            return
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        if len(self.player_bullet_list) < MAX_PLAYER_BULLETS:
            arcadeplus.play_sound(self.gun_sound)
            bullet = arcadeplus.Sprite(':resources:images/space_shooter/laserBlue01.png', SPRITE_SCALING_LASER)
            bullet.angle = 90
            bullet.change_y = BULLET_SPEED
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            self.player_bullet_list.append(bullet)

    def update_enemies(self):
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER:
                if self.enemy_change_x > 0:
                    self.enemy_change_x *= -1
                    move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        if move_down:
            for enemy in self.enemy_list:
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT
                if self.enemy_change_x > 0:
                    enemy.texture = self.enemy_textures[0]
                else:
                    enemy.texture = self.enemy_textures[1]

    def allow_enemies_to_fire(self):
        """
        See if any enemies will fire this frame.
        """
        x_spawn = []
        for enemy in self.enemy_list:
            chance = 4 + len(self.enemy_list) * 4
            if random.randrange(chance) == 0:
                if enemy.center_x not in x_spawn:
                    bullet = arcadeplus.Sprite(':resources:images/space_shooter/laserRed01.png', SPRITE_SCALING_LASER)
                    bullet.angle = 180
                    bullet.change_y = -BULLET_SPEED
                    bullet.center_x = enemy.center_x
                    bullet.top = enemy.bottom
                    self.enemy_bullet_list.append(bullet)
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):
        self.enemy_bullet_list.update()
        for bullet in self.enemy_bullet_list:
            hit_list = arcadeplus.check_for_collision_with_list(bullet, self.shield_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()

                continue
            if arcadeplus.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list):
                self.game_state = GAME_OVER
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def process_player_bullets(self):
        self.player_bullet_list.update()
        for bullet in self.player_bullet_list:
            hit_list = arcadeplus.check_for_collision_with_list(bullet, self.shield_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()

                continue
            hit_list = arcadeplus.check_for_collision_with_list(bullet, self.enemy_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1
                arcadeplus.play_sound(self.hit_sound)

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.game_state == GAME_OVER:
            return
        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()
        self.process_player_bullets()
        if len(self.enemy_list) == 0:
            self.setup_level_one()


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()