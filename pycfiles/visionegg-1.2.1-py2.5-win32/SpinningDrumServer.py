# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\SpinningDrumServer.py
# Compiled at: 2009-07-15 18:56:28
import VisionEgg, string, sys, os, math, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.Textures, VisionEgg.PyroHelpers, Pyro.core
from VisionEgg.PyroApps.ScreenPositionServer import ScreenPositionMetaController
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters
from VisionEgg.PyroApps.SpinningDrumGUI import SpinningDrumMetaParameters

class SpinningDrumExperimentMetaController(Pyro.core.ObjBase):

    def __init__(self, screen, presentation, stimuli):
        assert stimuli[0][0] == '3d_perspective'
        spinning_drum = stimuli[0][1]
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = SpinningDrumMetaParameters()
        if not isinstance(screen, VisionEgg.Core.Screen):
            raise ValueError('Expecting instance of VisionEgg.Core.Screen')
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        if not isinstance(spinning_drum, VisionEgg.Textures.SpinningDrum):
            raise ValueError('Expecting instance of VisionEgg.Textures.SpinningDrum')
        self.p = presentation
        self.stim = spinning_drum
        screen.parameters.bgcolor = (0.5, 0.5, 0.5, 0.0)
        self.p.add_controller(self.stim, 'on', VisionEgg.FlowControl.FunctionController(during_go_func=self.on_function_during_go, between_go_func=self.on_function_between_go))
        self.p.add_controller(self.stim, 'angular_position', VisionEgg.FlowControl.FunctionController(during_go_func=self.angular_position_during_go, between_go_func=self.angular_position_between_go))

    def __del__(self):
        self.p.remove_controller(self.stim, 'on')
        self.p.remove_controller(self.stim, 'angular_position')
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

    def angular_position_during_go(self, t):
        adjusted_t = t - self.meta_params.pre_stim_sec
        return adjusted_t * self.meta_params.velocity_dps + self.meta_params.startpos_deg

    def angular_position_between_go(self):
        return 0.0

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, SpinningDrumMetaParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of SpinningDrumMetaParameters')
        self.update()

    def update(self):
        stim_params = self.stim.parameters
        meta_params = self.meta_params
        stim_params.contrast = meta_params.contrast
        self.p.parameters.go_duration = (meta_params.pre_stim_sec + meta_params.stim_sec + meta_params.post_stim_sec, 'seconds')

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


def get_meta_controller_class():
    return SpinningDrumExperimentMetaController


def make_stimuli():
    filename = os.path.join(VisionEgg.config.VISIONEGG_SYSTEM_DIR, 'data/panorama.jpg')
    texture = VisionEgg.Textures.Texture(filename)
    stimulus = VisionEgg.Textures.SpinningDrum(texture=texture)
    return [('3d_perspective', stimulus)]


def get_meta_controller_stimkey():
    return 'spinning_drum_server'


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
    meta_controller = SpinningDrumExperimentMetaController(screen, p, stimuli)
    pyro_server.connect(meta_controller, get_meta_controller_stimkey())
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()