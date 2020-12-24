# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\DaqKeyboard.py
# Compiled at: 2009-07-07 11:29:42
"""
Data acquisition and triggering over the keyboard.

This module was programmed using information from the web site
http://www.pygame.org/docs/ref/pygame_key.html

"""
import VisionEgg, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.ParameterTypes as ve_types, sys, pygame
__version__ = VisionEgg.release_name

class KeyboardInput:

    def get_pygame_data(self):
        """Get keyboard input (return values are in pygame.locals.* notation)."""
        keys = pygame.key.get_pressed()
        return [ k for (k, v) in enumerate(keys) if v ]

    def get_string_data(self):
        """Get keyboard input (return values are converted to keyboard symbols (strings))."""
        pressed = self.get_pygame_data()
        keys_pressed = []
        for k in pressed:
            keys_pressed.append(pygame.key.name(k))

        return keys_pressed

    get_data = get_string_data


class KeyboardTriggerInController(VisionEgg.FlowControl.Controller):
    """Use the keyboard to trigger the presentation."""

    def __init__(self, key=pygame.locals.K_1):
        VisionEgg.FlowControl.Controller.__init__(self, return_type=ve_types.Integer, eval_frequency=VisionEgg.FlowControl.Controller.EVERY_FRAME)
        self.key = key

    def during_go_eval(self):
        return 1

    def between_go_eval(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.KEYDOWN:
                if event.key == self.key:
                    return 1
                else:
                    return 0