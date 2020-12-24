# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\FlatGratingServer.py
# Compiled at: 2009-07-15 18:56:28
"""Handle sinusoidal gratings (server-side)"""
import VisionEgg, string, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.Gratings, VisionEgg.PyroHelpers, Pyro.core
from VisionEgg.PyroApps.FlatGratingGUI import FlatGratingMetaParameters

class FlatGratingExperimentMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        assert stimuli[0][0] == '2d_overlay'
        grating = stimuli[0][1]
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = FlatGratingMetaParameters()
        if not isinstance(screen, VisionEgg.Core.Screen):
            raise ValueError('Expecting instance of VisionEgg.Core.Screen')
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        if not isinstance(grating, VisionEgg.Gratings.SinGrating2D):
            raise ValueError('Expecting instance of VisionEgg.Gratings.SinGrating2D')
        self.p = presentation
        self.stim = grating
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
        if isinstance(new_parameters, FlatGratingMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of FlatGratingMetaParameters')
        self.update()

    def update(self):
        stim_params = self.stim.parameters
        meta_params = self.meta_params
        stim_params.contrast = meta_params.contrast
        stim_params.orientation = meta_params.orient
        stim_params.spatial_freq = meta_params.sf
        stim_params.temporal_freq_hz = meta_params.tf
        stim_params.size = (meta_params.size_x, meta_params.size_y)
        stim_params.position = (meta_params.center_x, meta_params.center_y)
        self.p.parameters.go_duration = (meta_params.pre_stim_sec + meta_params.stim_sec + meta_params.post_stim_sec, 'seconds')

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return FlatGratingExperimentMetaController


def make_stimuli():
    stimulus = VisionEgg.Gratings.SinGrating2D(spatial_freq=1.0 / 100.0, temporal_freq_hz=1.0, anchor='center')
    return [
     (
      '2d_overlay', stimulus)]


def get_meta_controller_stimkey():
    return 'flat_grating_server'


if __name__ == '__main__':
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    stimuli = make_stimuli()
    stimulus = stimuli[0][1]
    viewport = VisionEgg.Core.Viewport(screen=screen, stimuli=[stimulus])
    p = VisionEgg.FlowControl.Presentation(viewports=[viewport])
    meta_controller = FlatGratingExperimentMetaController(screen, p, stimuli)
    pyro_server.connect(meta_controller, get_meta_controller_stimkey())
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()