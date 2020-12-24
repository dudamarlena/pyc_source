# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\view_pause_screen.py
# Compiled at: 2020-03-29 18:11:29
# Size of source mod 2**32: 5042 bytes
__doc__ = '\nThis program shows how to have a pause screen without resetting the game.\n\nMake a separate class for each view (screen) in your game.\nThe class will inherit from arcadeplus.View. The structure will\nlook like an arcadeplus.Window as each View will need to have its own draw,\nupdate and window event methods. To switch a View, simply create a view\nwith `view = MyView()` and then use the "self.window.set_view(view)" method.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.view_pause_screen\n'
import arcadeplus, os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5

class MenuView(arcadeplus.View):

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Menu Screen', (WIDTH / 2), (HEIGHT / 2), (arcadeplus.color.BLACK),
          font_size=50, anchor_x='center')
        arcadeplus.draw_text('Click to advance.', (WIDTH / 2), (HEIGHT / 2 - 75), (arcadeplus.color.GRAY),
          font_size=20, anchor_x='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView()
        self.window.show_view(game)


class GameView(arcadeplus.View):

    def __init__(self):
        super().__init__()
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)

    def on_draw(self):
        arcadeplus.start_render()
        self.player_sprite.draw()
        arcadeplus.draw_text('Press Esc. to pause', (WIDTH / 2),
          (HEIGHT - 100),
          (arcadeplus.color.BLACK),
          font_size=20,
          anchor_x='center')

    def on_update(self, delta_time):
        self.player_sprite.update()
        if self.player_sprite.left < 0 or self.player_sprite.right > WIDTH:
            self.player_sprite.change_x *= -1
        if self.player_sprite.bottom < 0 or self.player_sprite.top > HEIGHT:
            self.player_sprite.change_y *= -1

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)


class PauseView(arcadeplus.View):

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.ORANGE)

    def on_draw(self):
        arcadeplus.start_render()
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()
        arcadeplus.draw_lrtb_rectangle_filled(left=(player_sprite.left), right=(player_sprite.right),
          top=(player_sprite.top),
          bottom=(player_sprite.bottom),
          color=(arcadeplus.color.ORANGE + (200, )))
        arcadeplus.draw_text('PAUSED', (WIDTH / 2), (HEIGHT / 2 + 50), (arcadeplus.color.BLACK),
          font_size=50, anchor_x='center')
        arcadeplus.draw_text('Press Esc. to return', (WIDTH / 2),
          (HEIGHT / 2),
          (arcadeplus.color.BLACK),
          font_size=20,
          anchor_x='center')
        arcadeplus.draw_text('Press Enter to reset', (WIDTH / 2),
          (HEIGHT / 2 - 30),
          (arcadeplus.color.BLACK),
          font_size=20,
          anchor_x='center')

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcadeplus.key.ENTER:
            game = GameView()
            self.window.show_view(game)


def main():
    window = arcadeplus.Window(WIDTH, HEIGHT, 'Instruction and Game Over Views Example')
    menu = MenuView()
    window.show_view(menu)
    arcadeplus.run()


if __name__ == '__main__':
    main()