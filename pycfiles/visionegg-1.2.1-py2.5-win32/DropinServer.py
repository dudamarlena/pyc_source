# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\DropinServer.py
# Compiled at: 2009-07-07 11:29:42
import VisionEgg, string, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.Textures, VisionEgg.SphereMap, VisionEgg.PyroHelpers, Pyro.core
from VisionEgg.PyroApps.ScreenPositionServer import ScreenPositionMetaController
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters
from VisionEgg.PyroApps.DropinGUI import DropinMetaParameters

class DropinMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = DropinMetaParameters()
        self.p = presentation
        print 'DropinMetaController presentation', self.p

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        self.meta_params = new_parameters
        self.update()

    def update(self):
        pass

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return DropinMetaController


def make_stimuli():
    pass


def get_meta_controller_stimkey():
    return 'dropin_server'