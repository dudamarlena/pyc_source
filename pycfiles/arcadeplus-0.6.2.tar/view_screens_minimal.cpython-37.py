# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\view_screens_minimal.py
# Compiled at: 2020-03-29 18:11:32
# Size of source mod 2**32: 2923 bytes
__doc__ = '\nThis program shows how to:\n  * Display a sequence of screens in your game.  The "arcadeplus.View"\n    class makes it easy to separate the code for each screen into\n    its own class.\n  * This example shows the absolute basics of using "arcadeplus.View".\n    See the "different_screens_example.py" for how to handle\n    screen-specific data.\n\nMake a separate class for each view (screen) in your game.\nThe class will inherit from arcadeplus.View. The structure will\nlook like an arcadeplus.Window as each View will need to have its own draw,\nupdate and window event methods. To switch a View, simply create a View\nwith `view = MyView()` and then use the "self.window.set_view(view)" method.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.view_screens_minimal\n'
import arcadeplus, os
WIDTH = 800
HEIGHT = 600

class MenuView(arcadeplus.View):

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Menu Screen - click to advance', (WIDTH / 2), (HEIGHT / 2), (arcadeplus.color.BLACK),
          font_size=30, anchor_x='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcadeplus.View):

    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.ORANGE_PEEL)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Game - press SPACE to advance', (WIDTH / 2), (HEIGHT / 2), (arcadeplus.color.BLACK),
          font_size=30, anchor_x='center')

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)


class GameOverView(arcadeplus.View):

    def on_show(self):
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_draw(self):
        arcadeplus.start_render()
        arcadeplus.draw_text('Game Over - press ESCAPE to advance', (WIDTH / 2), (HEIGHT / 2), (arcadeplus.color.WHITE),
          30, anchor_x='center')

    def on_key_press(self, key, _modifiers):
        if key == arcadeplus.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcadeplus.Window(WIDTH, HEIGHT, 'Different Views Minimal Example')
    menu_view = MenuView()
    window.show_view(menu_view)
    arcadeplus.run()


if __name__ == '__main__':
    main()