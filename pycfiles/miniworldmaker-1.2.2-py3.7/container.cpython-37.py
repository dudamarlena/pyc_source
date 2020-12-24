# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\containers\container.py
# Compiled at: 2020-02-02 04:42:51
# Size of source mod 2**32: 3134 bytes
import logging, pygame

class Container:
    __doc__ = '\n    Base class for containers\n    '
    clog = logging.getLogger('Container')

    def __init__(self):
        self.dirty = 1
        self.surface = pygame.Surface((1, 1))
        self.background_color = (255, 255, 255)
        self.default_size = 100
        self.registered_events = {'mouse_left', 'mouse_right'}
        self._window = None
        self._container_width = 0
        self._container_height = 0
        self.container_top_left_x = 0
        self.container_top_left_y = 0
        self.docking_position = None
        self._image = None

    @property
    def container_width(self):
        return self._container_width

    @property
    def container_height(self):
        return self._container_height

    @property
    def window(self):
        return self._window

    def _add_to_window(self, window, dock, size=None):
        self._window = window
        if size == None:
            size = self.default_size
        elif dock == 'top_left':
            self.container_top_left_x = 0
            self.container_top_left_y = 0
            self.docking_position = dock
        else:
            if dock == 'right':
                self.container_top_left_x = self._window.window_width
                self.container_top_left_y = 0
                self.docking_position = dock
                self._container_height = self._window.window_height
                self._container_width = size
            else:
                if dock == 'bottom':
                    self.container_top_left_x = 0
                    self.container_top_left_y = self._window.window_height
                    self.docking_position = dock
                    self._container_width = self._window.window_width
                    self._container_height = size
        self.clog.info('Added Container {0} with width: {1} and height {2}'.format(self, self.width, self.height))
        self._image = pygame.Surface((self.width, self.height))

    @property
    def size(self):
        return (self._container_width, self._container_height)

    def repaint(self):
        pass

    def blit_surface_to_window_surface(self):
        self._window.window_surface.blit(self.surface, self.rect)

    def remove(self):
        pass

    def handle_event(self, event, data):
        self.get_event(event, data)

    def get_event(self, event, data):
        pass

    def is_in_container(self, x, y):
        if self.rect.collidepoint((x, y)):
            return True
        return False

    @property
    def rect(self):
        return pygame.Rect(self.container_top_left_x, self.container_top_left_y, self.width, self.height)

    @property
    def window_docking_position(self):
        return self.docking_position

    def update(self):
        pass

    @property
    def width(self):
        return self._container_width

    @property
    def height(self):
        return self._container_height