# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/widgets/button.py
# Compiled at: 2009-02-25 04:20:27
from bezel.graphics.widget import Widget
from bezel.graphics.containers import Bin
from bezel.graphics.widgets.text import Text
from bezel.graphics.widgets.image import Image
import pygame

class BaseButton(Widget):
    """A button container, which can be indented or outdented."""

    def __init__(self, callback, *args, **kwargs):
        super(BaseButton, self).__init__(*args, **kwargs)
        self.pushed = False
        self.action = callback

    def mouse_down(self, x, y, button):
        """Pushes in the button."""
        super(BaseButton, self).mouse_down(x, y, button)
        self.pushed = True
        self.invalidate()

    def mouse_up(self, x, y, button):
        """Releases the button and calls the action callback."""
        super(BaseButton, self).mouse_up(x, y, button)
        (width, height) = self.size
        self.pushed = False
        self.invalidate()
        if x >= 0 and x < width and y >= 0 and y < height:
            self.action()


class Button(BaseButton, Text):
    """A button with text."""

    def paint(self):
        if self.pushed:
            colour = (85, 87, 83)
        else:
            colour = (136, 138, 133)
        surface.fill(colour)
        pygame.draw.rect(surface, (46, 52, 54), surface.get_rect(), 2)
        super(Button, self).paint()


class ImageButton(BaseButton, Bin):

    def __init__(self, callback, normal_image, hover_image=None, pushed_image=None, *args, **kwargs):
        super(ImageButton, self).__init__(callback=callback, *args, **kwargs)
        self.normal_image = Image(normal_image)
        self.child = self.normal_image
        self.hover_image = self.pushed_image = self.normal_image
        if hover_image is not None:
            self.hover_image = Image(hover_image)
        if pushed_image is not None:
            self.pushed_image = Image(pushed_image)
        self.size = self.normal_image.size
        return

    def mouse_up(self, x, y, button):
        super(ImageButton, self).mouse_up(x, y, button)
        if self.mouse_inside:
            self.child = self.hover_image
        else:
            self.child = self.normal_image

    def mouse_down(self, x, y, button):
        super(ImageButton, self).mouse_down(x, y, button)
        self.child = self.pushed_image

    def mouse_enter(self, x, y, buttons):
        super(ImageButton, self).mouse_enter(x, y, buttons)
        self.child = self.hover_image

    def mouse_leave(self, x, y, buttons):
        super(ImageButton, self).mouse_leave(x, y, buttons)
        if self.pushed:
            self.child = self.pushed_image
        else:
            self.child = self.normal_image