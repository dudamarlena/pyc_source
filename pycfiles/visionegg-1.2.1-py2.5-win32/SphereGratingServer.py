# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\SphereGratingServer.py
# Compiled at: 2009-07-15 18:56:28
"""Handle perspective-distorted sinusoidal gratings (server-side)"""
import VisionEgg, string, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.SphereMap, VisionEgg.PyroHelpers, Pyro.core
from VisionEgg.PyroApps.ScreenPositionServer import ScreenPositionMetaController
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters
from VisionEgg.PyroApps.SphereGratingGUI import SphereGratingMetaParameters

class SphereGratingExperimentMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        assert stimuli[0][0] == '3d_perspective'
        assert stimuli[1][0] == '3d_perspective'
        sphere_grating = stimuli[0][1]
        sphere_window = stimuli[1][1]
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = SphereGratingMetaParameters()
        if not isinstance(screen, VisionEgg.Core.Screen):
            raise ValueError('Expecting instance of VisionEgg.Core.Screen')
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        if not isinstance(sphere_grating, VisionEgg.SphereMap.SphereGrating):
            raise ValueError('Expecting instance of VisionEgg.SphereMap.SphereGrating')
        if not isinstance(sphere_window, VisionEgg.SphereMap.SphereWindow):
            raise ValueError('Expecting instance of VisionEgg.SphereMap.SphereWindow')
        self.p = presentation
        self.stim = sphere_grating
        self.window = sphere_window
        screen.parameters.bgcolor = (0.5, 0.5, 0.5, 0.0)
        self.p.add_controller(self.stim, 'on', VisionEgg.FlowControl.FunctionController(during_go_func=self.on_function_during_go, between_go_func=self.on_function_between_go))

    def __del__(self):
        self.p.remove_controller(self.stim, 'on')
        Pyro.core.ObjBase.__del__(self)

    def on_function_during_go(self, t):
        """Compute when the grating is on"""
        if t <= self.meta_params.pre_stim_sec:
            return 0
        elif t <= self.meta_params.pre_stim_sec + self.meta_params.stim_sec:
            return 1
        else:
            return 0

    def on_function_between_go(self):
        """Compute when the grating is off"""
        return 0

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, SphereGratingMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of SphereGratingMetaParameters')
        self.update()

    def update(self):
        stim_params = self.stim.parameters
        window_params = self.window.parameters
        meta_params = self.meta_params
        stim_params.contrast = meta_params.contrast
        stim_params.orientation = meta_params.orient
        stim_params.spatial_freq_cpd = meta_params.sf
        stim_params.temporal_freq_hz = meta_params.tf
        stim_params.grating_center_azimuth = meta_params.window_az
        stim_params.grating_center_elevation = meta_params.window_el
        self.p.parameters.go_duration = (meta_params.pre_stim_sec + meta_params.stim_sec + meta_params.post_stim_sec, 'seconds')
        window_params.window_shape = meta_params.window_func
        window_params.window_shape_radius_parameter = meta_params.window_radius
        window_params.window_center_azimuth = meta_params.window_az
        window_params.window_center_elevation = meta_params.window_el

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return SphereGratingExperimentMetaController


def make_stimuli():
    stimulus = VisionEgg.SphereMap.SphereGrating(radius=1.0, spatial_freq_cpd=1.0 / 9.0, temporal_freq_hz=1.0)
    mask = VisionEgg.SphereMap.SphereWindow(radius=0.95)
    return [('3d_perspective', stimulus), ('3d_perspective', mask)]


def get_meta_controller_stimkey():
    return 'sphere_grating_server'


if __name__ == '__main__':
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    stimuli = make_stimuli()
    stimulus = stimuli[0][1]
    mask = stimuli[1][1]
    temp = ScreenPositionParameters()
    left = temp.left
    right = temp.right
    bottom = temp.bottom
    top = temp.top
    near = temp.near
    far = temp.far
    projection = VisionEgg.Core.PerspectiveProjection(left, right, bottom, top, near, far)
    viewport = VisionEgg.Core.Viewport(screen=screen, stimuli=[stimulus, mask], projection=projection)
    p = VisionEgg.FlowControl.Presentation(viewports=[viewport])
    projection_controller = ScreenPositionMetaController(p, projection)
    pyro_server.connect(projection_controller, 'projection_controller')
    meta_controller = SphereGratingExperimentMetaController(screen, p, stimuli)
    pyro_server.connect(meta_controller, get_meta_controller_stimkey())
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()