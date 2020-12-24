# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\ColorCalServer.py
# Compiled at: 2009-07-15 18:56:28
"""Handle luminance and color calibration stimulus (server-side)"""
import VisionEgg, string, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.PyroHelpers, Pyro.core, pygame, pygame.locals
from VisionEgg.PyroApps.ColorCalGUI import ColorCalMetaParameters

class ColorCalMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = ColorCalMetaParameters()
        if not isinstance(screen, VisionEgg.Core.Screen):
            raise ValueError('Expecting instance of VisionEgg.Core.Screen')
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        self.screen = screen
        self.p = presentation
        self.update()

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, ColorCalMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of ColorCalMetaParameters')
        self.update()

    def update(self):
        self.screen.parameters.bgcolor = self.meta_params.color

    def go(self):
        pass

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return ColorCalMetaController


def make_stimuli():
    return []


def get_meta_controller_stimkey():
    return 'color_cal_server'


if __name__ == '__main__':
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    p = VisionEgg.FlowControl.Presentation()
    stimuli = make_stimuli()
    meta_controller = ColorCalMetaController(screen, p, stimuli)
    pyro_server.connect(meta_controller, get_meta_controller_stimkey())
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()