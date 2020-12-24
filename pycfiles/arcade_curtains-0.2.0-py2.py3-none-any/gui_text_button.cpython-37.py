# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\gui_text_button.py
# Compiled at: 2020-03-29 18:05:33
# Size of source mod 2**32: 7684 bytes
__doc__ = '\nButtons with text on them\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.gui_text_button\n'
import arcadeplus, random, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'GUI Text Buton Example'

class TextButton:
    """TextButton"""

    def __init__(self, center_x, center_y, width, height, text, font_size=18, font_face='Arial', face_color=arcadeplus.color.LIGHT_GRAY, highlight_color=arcadeplus.color.WHITE, shadow_color=arcadeplus.color.GRAY, button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcadeplus.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)
        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color
        arcadeplus.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y - self.height / 2, color, self.button_height)
        arcadeplus.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color, self.button_height)
        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color
        arcadeplus.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2, self.center_x + self.width / 2, self.center_y + self.height / 2, color, self.button_height)
        arcadeplus.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2, self.center_x - self.width / 2, self.center_y + self.height / 2, color, self.button_height)
        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height
        arcadeplus.draw_text((self.text), x, y, (arcadeplus.color.BLACK),
          font_size=(self.font_size), width=(self.width),
          align='center',
          anchor_x='center',
          anchor_y='center')

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class StartTextButton(TextButton):

    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, 'Start', 18, 'Arial')
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class StopTextButton(TextButton):

    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, 'Stop', 18, 'Arial')
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.pause = False
        self.coin_list = None
        self.button_list = None

    def setup(self):
        self.coin_list = arcadeplus.SpriteList()
        for i in range(10):
            coin = arcadeplus.Sprite(':resources:images/items/coinGold.png', 0.25)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.change_y = -1
            self.coin_list.append(coin)

        self.button_list = []
        play_button = StartTextButton(60, 570, self.resume_program)
        self.button_list.append(play_button)
        quit_button = StopTextButton(60, 515, self.pause_program)
        self.button_list.append(quit_button)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        self.coin_list.draw()
        for button in self.button_list:
            button.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.pause:
            return
        self.coin_list.update()
        for coin in self.coin_list:
            if coin.top < 0:
                coin.bottom = SCREEN_HEIGHT

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        check_mouse_release_for_buttons(x, y, self.button_list)

    def pause_program(self):
        self.pause = True

    def resume_program(self):
        self.pause = False


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()