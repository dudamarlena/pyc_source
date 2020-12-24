# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\view_instructions_and_game_over.py
# Compiled at: 2020-03-29 18:11:25
# Size of source mod 2**32: 6530 bytes
__doc__ = "\nThis program shows how to:\n  * Have one or more instruction screens\n  * Show a 'Game over' text and halt the game\n  * Allow the user to restart the game\n\nMake a separate class for each view (screen) in your game.\nThe class will inherit from arcadeplus.View. The structure will\nlook like an arcadeplus.Window as each view will need to have its own draw,\nupdate and window event methods. To switch a view, simply create a view\nwith `view = MyView()` and then use the view.show() method.\n\nThis example shows how you can set data from one View on another View to pass data\naround (see: time_taken), or you can store data on the Window object to share data between\nall Views (see: total_score).\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.view_instructions_and_game_over.py\n"
import arcadeplus, random, os
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
        arcadeplus.draw_text('Click to advance', (WIDTH / 2), (HEIGHT / 2 - 75), (arcadeplus.color.GRAY),
          font_size=20, anchor_x='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcadeplus.View):

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.ORANGE_PEEL)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Instructions Screen', (WIDTH / 2), (HEIGHT / 2), (arcadeplus.color.BLACK),
          font_size=50, anchor_x='center')
        arcadeplus.draw_text('Click to advance', (WIDTH / 2), (HEIGHT / 2 - 75), (arcadeplus.color.GRAY),
          font_size=20, anchor_x='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcadeplus.View):

    def __init__(self):
        super().__init__()
        self.time_taken = 0
        self.player_list = arcadeplus.SpriteList()
        self.coin_list = arcadeplus.SpriteList()
        self.score = 0
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        for i in range(5):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', SPRITE_SCALING / 3)
            coin.center_x = random.randrange(WIDTH)
            coin.center_y = random.randrange(HEIGHT)
            self.coin_list.append(coin)

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.window.set_mouse_visible(False)

    def on_draw(self):
        arcadeplus.start_render()
        self.player_list.draw()
        self.coin_list.draw()
        output = f"Score: {self.score}"
        arcadeplus.draw_text(output, 10, 30, arcadeplus.color.WHITE, 14)
        output_total = f"Total Score: {self.window.total_score}"
        arcadeplus.draw_text(output_total, 10, 10, arcadeplus.color.WHITE, 14)

    def on_update(self, delta_time):
        self.time_taken += delta_time
        self.coin_list.update()
        self.player_list.update()
        hit_list = arcadeplus.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list:
            coin.kill()
            self.score += 1
            self.window.total_score += 1

        if len(self.coin_list) == 0:
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


class GameOverView(arcadeplus.View):

    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Game Over', 240, 400, arcadeplus.color.WHITE, 54)
        arcadeplus.draw_text('Click to restart', 310, 300, arcadeplus.color.WHITE, 24)
        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcadeplus.draw_text(f"Time taken: {time_taken_formatted}", (WIDTH / 2),
          200,
          (arcadeplus.color.GRAY),
          font_size=15,
          anchor_x='center')
        output_total = f"Total Score: {self.window.total_score}"
        arcadeplus.draw_text(output_total, 10, 10, arcadeplus.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcadeplus.Window(WIDTH, HEIGHT, 'Different Views Example')
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcadeplus.run()


if __name__ == '__main__':
    main()