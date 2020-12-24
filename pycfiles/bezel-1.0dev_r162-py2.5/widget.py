# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/widget.py
# Compiled at: 2009-02-25 04:20:27
import pygame
from bezel.misc import InheritProperty

class Widget(object):
    """
    A widget is the base unit of graphics - all other
    graphical objects subclass Widget.

    A widget has a position and size, and a surface.
    """

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.surface = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.mouse_grabbed = False
        self.mouse_inside = False
        return

    def _pump(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.key_down(event.key, event.unicode, event.mod)
            elif event.type == pygame.KEYUP:
                try:
                    char = chr(event.key)
                except ValueError:
                    char = ''
                else:
                    self.key_up(event.key, char, event.mod)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = event.pos
                if self.rect.collidepoint(x, y):
                    x -= self.rect.x
                    y -= self.rect.y
                    self.mouse_down(x, y, event.button)
                self.mouse_grabbed = True
            elif event.type == pygame.MOUSEMOTION:
                (x, y) = event.pos
                if self.mouse_inside or self.mouse_grabbed or self.rect.collidepoint(x, y):
                    x -= self.rect.x
                    y -= self.rect.y
                    self.mouse_move(x, y, event.buttons)
            elif event.type == pygame.MOUSEBUTTONUP:
                (x, y) = event.pos
                if self.mouse_grabbed or self.rect.collidepoint(x, y):
                    x -= self.rect.x
                    y -= self.rect.y
                    self.mouse_up(x, y, event.button)
                self.mouse_grabbed = False

    def key_down(self, key, char, mod):
        pass

    def key_up(self, key, char, mod):
        pass

    def mouse_down(self, x, y, button):
        pass

    def mouse_up(self, x, y, button):
        pass

    def mouse_move(self, x, y, buttons):
        (width, height) = self.size
        if x >= 0:
            if y >= 0 and x < width and y < height:
                self.mouse_inside = self.mouse_inside or True
                self.mouse_enter(x, y, buttons)
        elif self.mouse_inside:
            self.mouse_inside = False
            self.mouse_leave(x, y, buttons)

    def mouse_enter(self, x, y, buttons):
        pass

    def mouse_leave(self, x, y, buttons):
        pass

    started = False

    def paint(self):
        """Paint the sprite onto self.surface."""
        pass

    def draw(self, surface, dirty):
        """Draws self.surface onto the surface.
        
        Note: If overriding, this method should be
        as optimised as possible."""
        if self.surface:
            widget = self.surface
            surface_blit = surface.blit
            (x, y) = self.rect.topleft
            for rect in dirty:
                clip = rect.move((-x, -y))
                surface_blit(widget, (rect.x, rect.y), clip)

        else:
            surface.fill((238, 238, 236), self.rect)

    def invalidate(self, rect=None):
        if self.parent is None:
            return
        if rect is None:
            rect = self.rect
        else:
            rect = rect.clip(self.rect)
        self.parent.invalidate(rect)
        return

    def update(self, delay):
        """Update the sprite's movement, etc. each frame.
        
        delay: The number of milliseconds since the last update.
        """
        pass

    __parent = None

    def get_parent(self):
        return self.__parent

    def set_parent(self, parent):
        self.__parent = parent
        if parent is not None and self not in parent:
            parent.add(self)
        return

    parent = InheritProperty(get_parent, set_parent)
    _position = (0, 0)

    def get_position(self):
        return self._position

    def set_position(self, position):
        previous = self._position
        self._position = position
        if self.parent is not None and previous != position:
            self.parent.paint()
        return

    position = InheritProperty(get_position, set_position)
    _size = (0, 0)

    def get_size(self):
        return self._size

    def set_size(self, size):
        previous = self._size
        self._size = size
        if self.parent is not None and previous != size:
            self.parent.paint()
        return

    size = InheritProperty(get_size, set_size)