# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\gui_dialogue_box.py
# Compiled at: 2020-03-29 18:05:26
# Size of source mod 2**32: 4000 bytes
import os, arcadeplus

class ShowButton(arcadeplus.gui.TextButton):

    def __init__(self, dialoguebox, x, y, width=110, height=50, text='Show', theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if not self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.dialoguebox.active = True


class CloseButton(arcadeplus.gui.TextButton):

    def __init__(self, dialoguebox, x, y, width=110, height=50, text='Close', theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.dialoguebox = dialoguebox

    def on_press(self):
        if self.dialoguebox.active:
            self.pressed = True

    def on_release(self):
        if self.pressed:
            if self.dialoguebox.active:
                self.pressed = False
                self.dialoguebox.active = False


class Window(arcadeplus.Window):

    def __init__(self):
        super().__init__()
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.theme = None

    def add_dialogue_box(self):
        color = (220, 228, 255)
        dialoguebox = arcadeplus.gui.DialogueBox(self.half_width, self.half_height, self.half_width * 1.1, self.half_height * 1.5, color, self.theme)
        close_button = CloseButton(dialoguebox, (self.half_width), (self.half_height - self.half_height / 2 + 40), theme=(self.theme))
        dialoguebox.button_list.append(close_button)
        message = 'Hello I am a Dialogue Box.'
        dialoguebox.text_list.append(arcadeplus.gui.TextBox(message, self.half_width, self.half_height, self.theme.font_color))
        self.dialogue_box_list.append(dialoguebox)

    def add_text(self):
        message = 'Press this button to activate the Dialogue Box'
        self.text_list.append(arcadeplus.gui.TextBox(message, self.half_width - 50, self.half_height))

    def add_button(self):
        show_button = ShowButton((self.dialogue_box_list[0]), (self.width - 100), (self.half_height), theme=(self.theme))
        self.button_list.append(show_button)

    def set_dialogue_box_texture(self):
        dialogue_box = ':resources:gui_themes/Fantasy/DialogueBox/DialogueBox.png'
        self.theme.add_dialogue_box_texture(dialogue_box)

    def set_button_texture(self):
        normal = ':resources:gui_themes/Fantasy/Buttons/Normal.png'
        hover = ':resources:gui_themes/Fantasy/Buttons/Hover.png'
        clicked = ':resources:gui_themes/Fantasy/Buttons/Clicked.png'
        locked = ':resources:gui_themes/Fantasy/Buttons/Locked.png'
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def set_theme(self):
        self.theme = arcadeplus.gui.Theme()
        self.set_dialogue_box_texture()
        self.set_button_texture()
        self.theme.set_font(24, arcadeplus.color.WHITE)

    def setup(self):
        arcadeplus.set_background_color(arcadeplus.color.ALICE_BLUE)
        self.set_theme()
        self.add_dialogue_box()
        self.add_text()
        self.add_button()

    def on_draw(self):
        arcadeplus.start_render()
        super().on_draw()

    def on_update(self, delta_time):
        if self.dialogue_box_list[0].active:
            return


def main():
    window = Window()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()