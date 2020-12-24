# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/display.py
# Compiled at: 2009-02-25 04:20:27
import pygame
from bezel.graphics.stage import Stage

class Display(Stage):
    """The Display class manages the underlying driver (e.g.: Pygame)
    to paint it's child onto the screen."""

    def __init__(self, title, icon=None, resizable=True, fullscreen=False, framerate=24, show_fps=False):
        super(Display, self).__init__()
        self.title = title
        if icon is not None:
            icon = pygame.image.load(icon)
        self.icon = icon
        self.resizable = resizable
        self.fullscreen = fullscreen
        self.framerate = framerate
        self.show_fps = show_fps
        self.dirty = []
        self.running = False
        pygame.display.set_caption(self.title)
        if self.icon is not None:
            pygame.display.set_icon(self.icon)
        self.resize()
        return

    def resize(self, size=None):
        """Resize the display to the specified width and height.
        May not work with all drivers.
        Returns True if resized, and False if resizing failed."""
        flags = 0
        if self.resizable:
            flags |= pygame.RESIZABLE
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
        if size is None:
            if self.fullscreen:
                size = pygame.display.list_modes()[0]
            else:
                size = (800, 600)
        self.surface = pygame.display.set_mode(size, flags)
        self.rect = pygame.Rect((0, 0), self.surface.get_size())
        self.paint()
        return

    def update_child(self):
        if len(self.scene_stack) < 1:
            self.quit()
        else:
            super(Display, self).update_child()

    def quit(self):
        """Closes the display by ending the event loop."""
        self.running = False

    def _pump(self, events):
        super(Display, self)._pump(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
                resize = event.size
            elif event.type == pygame.VIDEOEXPOSE:
                self.invalidate()

    def invalidate(self, rect=None):
        if rect is None:
            rect = self.rect
        else:
            rect = pygame.Rect(rect)
        self.dirty.append(rect)
        return

    def reduce_dirty(self):
        sprite_dirty = self.dirty
        sprite_dirty_pop = sprite_dirty.pop
        sprite_dirty_remove = sprite_dirty.remove
        rects = []
        rects_append = rects.append
        while sprite_dirty:
            rect = sprite_dirty_pop()
            rect_union_ip = rect.union_ip
            rect_collidelistall = rect.collidelistall
            overlaps = [ sprite_dirty[i] for i in rect_collidelistall(sprite_dirty)
                       ]
            while overlaps != []:
                for overlap in overlaps:
                    rect_union_ip(overlap)
                    sprite_dirty_remove(overlap)

                overlaps = [ sprite_dirty[i] for i in rect_collidelistall(sprite_dirty) ]

            rects_append(rect)

        self.dirty = rects

    def run(self):
        """Run the display."""
        self.running = True
        self.paint()
        update_clock = 0
        update_delay = 0
        if self.framerate:
            update_delay = 1000.0 / self.framerate
        clock = pygame.time.Clock()
        while self.running:
            if self.dirty:
                self.reduce_dirty()
            if self.dirty:
                for r in self.dirty:
                    self.surface.fill((0, 0, 0), r)

                self.draw(self.surface, self.dirty)
                pygame.display.update(self.dirty)
            self.dirty = []
            if self.framerate:
                delay = clock.tick(self.framerate)
            else:
                delay = clock.tick()
            update_clock += delay
            if update_clock >= update_delay:
                fps = 1000.0 / max([update_clock, 1])
                if self.show_fps:
                    print fps
                self.update(update_clock)
                update_clock = 0
                events = pygame.event.get()
                self._pump(events)

        pygame.display.quit()