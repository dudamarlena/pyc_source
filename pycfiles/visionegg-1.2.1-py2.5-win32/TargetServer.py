# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\TargetServer.py
# Compiled at: 2009-07-15 18:56:28
"""Handle small targets gratings (server-side)"""
import VisionEgg, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.MoreStimuli, VisionEgg.PyroHelpers, Pyro.core
from VisionEgg.PyroApps.TargetGUI import TargetMetaParameters

class TargetExperimentMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        Pyro.core.ObjBase.__init__(self)
        assert stimuli[0][0] == '2d_overlay'
        target = stimuli[0][1]
        self.meta_params = TargetMetaParameters()
        if not isinstance(screen, VisionEgg.Core.Screen):
            raise ValueError('Expecting instance of VisionEgg.Core.Screen')
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        if not isinstance(target, VisionEgg.MoreStimuli.Target2D):
            raise ValueError('Expecting instance of VisionEgg.MoreStimuli.Target2D')
        self.screen = screen
        self.p = presentation
        self.stim = target
        self.p.add_controller(self.stim, 'on', VisionEgg.FlowControl.FunctionController(during_go_func=self.on_function_during_go, between_go_func=self.on_function_between_go))
        self.p.add_controller(self.stim, 'position', VisionEgg.FlowControl.FunctionController(during_go_func=self.center_during_go, between_go_func=self.center_between_go))
        self.update()

    def __del__(self):
        self.p.remove_controller(self.stim, 'on')
        self.p.remove_controller(self.stim, 'position')
        Pyro.core.ObjBase.__del__(self)

    def on_function_during_go(self, t):
        if t <= self.meta_params.pre_stim_sec:
            return 0
        elif t <= self.meta_params.pre_stim_sec + self.meta_params.stim_sec:
            return 1
        else:
            return 0

    def on_function_between_go(self):
        return 0

    def center_during_go(self, t):
        t_adjusted = t - self.meta_params.pre_stim_sec
        distance = self.meta_params.velocity_pps * t_adjusted
        x_offset = math.cos(self.meta_params.direction_deg / 180.0 * math.pi) * distance
        y_offset = math.sin(self.meta_params.direction_deg / 180.0 * math.pi) * distance
        return (
         self.meta_params.start_x + x_offset,
         self.meta_params.start_y + y_offset)

    def center_between_go(self):
        return (0.0, 0.0)

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, TargetMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of TargetMetaParameters')
        self.update()

    def update(self):
        stim_params = self.stim.parameters
        meta_params = self.meta_params
        stim_params.color = meta_params.color
        self.screen.parameters.bgcolor = meta_params.bgcolor
        stim_params.size = (
         meta_params.width, meta_params.height)
        stim_params.orientation = meta_params.orientation_deg
        self.p.parameters.go_duration = (
         meta_params.pre_stim_sec + meta_params.stim_sec + meta_params.post_stim_sec, 'seconds')

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return TargetExperimentMetaController


def make_stimuli():
    stimulus = VisionEgg.MoreStimuli.Target2D(anchor='center')
    return [('2d_overlay', stimulus)]


def get_meta_controller_stimkey():
    return 'target_server'


if __name__ == '__main__':
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    stimuli = make_stimuli()
    stimulus = stimuli[0][1]
    viewport = VisionEgg.Core.Viewport(screen=screen, stimuli=[stimulus])
    p = VisionEgg.FlowControl.Presentation(viewports=[viewport])
    meta_controller = TargetExperimentMetaController(screen, p, stimuli)
    pyro_server.connect(meta_controller, get_meta_controller_stimkey())
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()