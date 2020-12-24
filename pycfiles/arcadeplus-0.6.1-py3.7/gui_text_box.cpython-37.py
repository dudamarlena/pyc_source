# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\gui_text_box.py
# Compiled at: 2020-03-29 18:05:29
# Size of source mod 2**32: 1155 bytes
import arcadeplus

class Window(arcadeplus.Window):

    def __init__(self):
        super().__init__(800, 600)
        self.text = ''
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    def setup(self):
        arcadeplus.set_background_color(arcadeplus.color.AMETHYST)
        self.text_list.append(arcadeplus.TextLabel('Name: ', self.center_x - 225, self.center_y))
        self.textbox_list.append(arcadeplus.TextBox(self.center_x - 125, self.center_y))
        self.button_list.append(arcadeplus.SubmitButton(self.textbox_list[0], self.on_submit, self.center_x, self.center_y))

    def on_draw(self):
        arcadeplus.start_render()
        super().on_draw()
        if self.text:
            arcadeplus.draw_text(f"Hello {self.text}", 400, 100, arcadeplus.color.BLACK, 24)

    def on_submit(self):
        self.text = self.textbox_list[0].text_storage.text


def main():
    window = Window()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()