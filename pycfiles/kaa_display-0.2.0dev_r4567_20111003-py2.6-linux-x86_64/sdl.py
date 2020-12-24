# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/display/sdl.py
# Compiled at: 2008-01-18 10:37:26
import pygame, pygame.locals, time, kaa, _SDL

class PygameDisplay(object):

    def __init__(self, size):
        if not pygame.display.get_init():
            pygame.display.init()
            pygame.font.init()
        self._screen = pygame.display.set_mode(size, 0, 32)
        if self._screen.get_bitsize() != 32:
            self._surface = pygame.Surface(size, 0, 32)
        else:
            self._surface = None
        self.signals = {'key_press_event': kaa.Signal(), 'mouse_up_event': kaa.Signal(), 
           'mouse_down_event': kaa.Signal()}
        kaa.main.signals['step'].connect(self.poll)
        pygame.key.set_repeat(500, 30)
        self.hide_mouse = True
        self.mousehidetime = time.time()
        return

    def render_imlib2_image(self, image, areas=None):
        """
        Render image to pygame surface. The image size must be the same size
        as the pygame window or it will crash. The optional parameter areas
        is a list of pos, size of the areas to update.
        """
        if self._surface:
            _SDL.image_to_surface(image, self._surface)
            if areas == None:
                self._screen.blit(self._surface, (0, 0))
            else:
                for (pos, size) in areas:
                    self._screen.blit(self._surface, pos, pos + size)

        else:
            _SDL.image_to_surface(image, self._screen)
        if areas:
            pygame.display.update(areas)
        else:
            pygame.display.update()
        return

    def poll(self):
        """
        Pygame poll function to get events.
        """
        if not pygame.display.get_init():
            return True
        if self.hide_mouse:
            mouserel = pygame.mouse.get_rel()
            mousedist = (mouserel[0] ** 2 + mouserel[1] ** 2) ** 0.5
            if mousedist > 4.0:
                pygame.mouse.set_visible(1)
                self.mousehidetime = time.time() + 1.0
            elif time.time() > self.mousehidetime:
                pygame.mouse.set_visible(0)
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.locals.NOEVENT:
                pass
            else:
                return True
                if event.type == pygame.locals.KEYDOWN:
                    self.signals['key_press_event'].emit(event.key)
                if event.type == pygame.locals.MOUSEBUTTONDOWN:
                    self.signals['mouse_down_event'].emit(event.button, event.pos)
                if event.type == pygame.locals.MOUSEBUTTONUP:
                    self.signals['mouse_up_event'].emit(event.button, event.pos)