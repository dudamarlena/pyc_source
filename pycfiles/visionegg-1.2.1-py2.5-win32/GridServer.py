# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\GridServer.py
# Compiled at: 2009-07-15 18:56:28
import VisionEgg, string, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.Textures, VisionEgg.SphereMap, VisionEgg.PyroHelpers, Pyro.core
from VisionEgg.PyroApps.ScreenPositionServer import ScreenPositionMetaController
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters
from VisionEgg.PyroApps.GridGUI import GridMetaParameters

class GridMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        assert stimuli[0][0] == '3d_perspective_with_set_viewport_callback'
        grid = stimuli[0][1]
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = GridMetaParameters()
        if not isinstance(screen, VisionEgg.Core.Screen):
            raise ValueError('Expecting instance of VisionEgg.Core.Screen')
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        if not isinstance(grid, VisionEgg.SphereMap.AzElGrid):
            raise ValueError('Expecting instance of VisionEgg.SphereMap.SphereMap')
        self.p = presentation
        self.stim = grid
        screen.parameters.bgcolor = (1.0, 1.0, 1.0, 0.0)

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, GridMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of GridMetaParameters')
        self.update()

    def update(self):
        self.p.parameters.go_duration = (0.0, 'seconds')

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return GridMetaController


def make_stimuli():
    stimulus = VisionEgg.SphereMap.AzElGrid()

    def set_az_el_grid_viewport(viewport):
        stimulus.parameters.my_viewport = viewport

    return [('3d_perspective_with_set_viewport_callback', stimulus, set_az_el_grid_viewport)]


def get_meta_controller_stimkey():
    return 'grid_server'


if __name__ == '__main__':
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    stimuli = make_stimuli()
    stimulus = stimuli[0][1]
    temp = ScreenPositionParameters()
    projection = VisionEgg.Core.PerspectiveProjection(temp.left, temp.right, temp.bottom, temp.top, temp.near, temp.far)
    viewport = VisionEgg.Core.Viewport(screen=screen, stimuli=[stimulus], projection=projection)
    p = VisionEgg.FlowControl.Presentation(viewports=[viewport])
    projection_controller = ScreenPositionMetaController(p, projection)
    pyro_server.connect(projection_controller, 'projection_controller')
    meta_controller = GridMetaController(screen, p, stimuli)
    pyro_server.connect(meta_controller, get_meta_controller_stimkey())
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()