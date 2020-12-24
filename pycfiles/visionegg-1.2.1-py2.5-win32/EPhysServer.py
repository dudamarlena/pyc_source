# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\EPhysServer.py
# Compiled at: 2009-07-15 18:56:28
import VisionEgg, sys, os, math, parser, symbol, token, compiler, tkMessageBox, pygame.display, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.SphereMap, VisionEgg.Text, VisionEgg.Textures, VisionEgg.PyroHelpers, Pyro, Pyro.core, VisionEgg.PyroApps.AST_ext as AST_ext, VisionEgg.PyroApps.TargetServer, VisionEgg.PyroApps.MouseTargetServer, VisionEgg.PyroApps.FlatGratingServer, VisionEgg.PyroApps.SphereGratingServer, VisionEgg.PyroApps.SpinningDrumServer, VisionEgg.PyroApps.GridServer, VisionEgg.PyroApps.ColorCalServer, VisionEgg.PyroApps.DropinServer
server_modules = [
 VisionEgg.PyroApps.TargetServer,
 VisionEgg.PyroApps.MouseTargetServer,
 VisionEgg.PyroApps.FlatGratingServer,
 VisionEgg.PyroApps.SphereGratingServer,
 VisionEgg.PyroApps.SpinningDrumServer,
 VisionEgg.PyroApps.GridServer,
 VisionEgg.PyroApps.ColorCalServer,
 VisionEgg.PyroApps.DropinServer]
from VisionEgg.PyroApps.ScreenPositionServer import ScreenPositionMetaController
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters

class EPhysServer(Pyro.core.ObjBase):

    def __init__(self, presentation, server_modules):
        Pyro.core.ObjBase.__init__(self)
        self.stimdict = {}
        self.stimkey = server_modules[0].get_meta_controller_stimkey()
        self.quit_status = False
        self.exec_demoscript_flag = False
        self.presentation = presentation
        self.onset_cal_bg = VisionEgg.MoreStimuli.Target2D(color=(0.0, 0.0, 0.0, 1.0), position=(30.0,
                                                                                                 30.0), anchor='center', size=(50.0,
                                                                                                                               50.0))
        self.onset_cal_fg = VisionEgg.MoreStimuli.Target2D(on=0, color=(1.0, 1.0, 1.0,
                                                                        1.0), position=(30.0,
                                                                                        30.0), anchor='center', size=(50.0,
                                                                                                                      50.0))
        self.presentation.add_controller(self.onset_cal_fg, 'on', VisionEgg.FlowControl.ConstantController(during_go_value=1, between_go_value=0))
        self.onset_cal_screen = self.presentation.parameters.viewports[0].parameters.screen
        self.onset_cal_viewport = VisionEgg.Core.Viewport(screen=self.onset_cal_screen, stimuli=[
         self.onset_cal_bg,
         self.onset_cal_fg])
        for server_module in server_modules:
            stimkey = server_module.get_meta_controller_stimkey()
            klass = server_module.get_meta_controller_class()
            make_stimuli = server_module.make_stimuli
            self.stimdict[stimkey] = (klass, make_stimuli)

    def __del__(self):
        self.presentation.remove_controller(self.onset_cal_fg, 'on')
        Pyro.core.ObjBase.__del__(self)

    def get_quit_status(self):
        return self.quit_status

    def set_quit_status(self, quit_status):
        self.quit_status = quit_status
        self.presentation.parameters.quit = quit_status

    def first_connection(self):
        self.presentation.parameters.quit = True

    def set_stim_onset_cal(self, on):
        if on:
            if self.onset_cal_viewport not in self.presentation.parameters.viewports:
                self.presentation.parameters.viewports.append(self.onset_cal_viewport)
        elif self.onset_cal_viewport in self.presentation.parameters.viewports:
            self.presentation.parameters.viewports.remove(self.onset_cal_viewport)

    def set_stim_onset_cal_location(self, center, size):
        self.onset_cal_bg.parameters.position = center
        self.onset_cal_fg.parameters.position = center
        self.onset_cal_bg.parameters.size = size
        self.onset_cal_fg.parameters.size = (size[0] - 2, size[1] - 2)

    def get_stim_onset_cal_location(self):
        (x, y) = self.onset_cal_bg.parameters.position
        (width, height) = self.onset_cal_bg.parameters.size
        return (x, y, width, height)

    def set_gamma_ramp(self, red, blue, green):
        return pygame.display.set_gamma_ramp(red, green, blue)

    def is_in_go_loop(self):
        return self.presentation.is_in_go_loop()

    def were_frames_dropped_in_last_go_loop(self):
        return self.presentation.were_frames_dropped_in_last_go_loop()

    def get_last_go_loop_start_time_absolute_sec(self):
        return self.presentation.get_last_go_loop_start_time_absolute_sec()

    def set_override_t_abs_sec(self, value_sec_string):
        value_sec = float(value_sec_string)
        self.presentation.parameters.override_t_abs_sec = value_sec

    def get_next_stimulus_meta_controller(self):
        if self.stimkey:
            (klass, make_stimuli) = self.stimdict[self.stimkey]
            stimuli = make_stimuli()
            return (self.stimkey, klass, stimuli)
        else:
            raise RuntimeError('No stimkey')

    def get_stimkey(self):
        return self.stimkey

    def set_next_stimkey(self, stimkey):
        self.stimkey = stimkey

    def get_cwd(self):
        return os.path.abspath(os.curdir)

    def save_image_sequence(self, fps=12.0, filename_base='im', filename_suffix='.tif', save_dir='.'):
        try:
            self.presentation.export_movie_go(frames_per_sec=fps, filename_base=filename_base, filename_suffix=filename_suffix, path=save_dir)
        except Exception, x:
            import traceback
            traceback.print_exc()
            raise

    def build_AST(self, source):
        AST = parser.suite(source)
        self.AST = AST

    def exec_AST(self, screen, dropin_meta_params):
        if dropin_meta_params.vars_list is not None:
            for var in dropin_meta_params.vars_list:
                self.AST = AST_ext.modify_AST(self.AST, var[0], var[1])

        code_module = self.AST.compile()
        exec code_module in locals()
        self.script_dropped_frames = p.were_frames_dropped_in_last_go_loop()
        self.presentation.last_go_loop_start_time_absolute_sec = p.last_go_loop_start_time_absolute_sec
        self.exec_demoscript_flag = False
        return

    def run_demoscript(self):
        self.exec_demoscript_flag = True


def start_server(server_modules, server_class=EPhysServer):
    loadNewExpr = True
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    temp = ScreenPositionParameters()
    projection = VisionEgg.Core.PerspectiveProjection(temp.left, temp.right, temp.bottom, temp.top, temp.near, temp.far)
    perspective_viewport = VisionEgg.Core.Viewport(screen=screen, projection=projection)
    overlay2D_viewport = VisionEgg.Core.Viewport(screen=screen)
    p = VisionEgg.FlowControl.Presentation(viewports=[perspective_viewport, overlay2D_viewport])
    print 'main Presentation', p
    wait_text = VisionEgg.Text.Text(text='Starting up...', position=(
     screen.size[0] / 2.0, 5), anchor='bottom', color=(1.0, 0.0, 0.0, 0.0))
    overlay2D_viewport.parameters.stimuli = [
     wait_text]
    p.between_presentations()
    projection_controller = ScreenPositionMetaController(p, projection)
    pyro_server.connect(projection_controller, 'projection_controller')
    ephys_server = server_class(p, server_modules)
    pyro_server.connect(ephys_server, 'ephys_server')
    (hostname, port) = pyro_server.get_hostname_and_port()
    wait_text.parameters.text = 'Waiting for connection at %s port %d' % (hostname, port)
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()
    wait_text.parameters.text = 'Loading new experiment, please wait.'
    while not ephys_server.get_quit_status():
        if loadNewExpr:
            wait_text.parameters.text = 'Loading new experiment, please wait.'
            perspective_viewport.parameters.stimuli = []
            overlay2D_viewport.parameters.stimuli = [wait_text]
            p.between_presentations()
            (pyro_name, meta_controller_class, stimulus_list) = ephys_server.get_next_stimulus_meta_controller()
            stimulus_meta_controller = meta_controller_class(screen, p, stimulus_list)
            pyro_server.connect(stimulus_meta_controller, pyro_name)
        if ephys_server.get_stimkey() == 'dropin_server':
            wait_text.parameters.text = 'Vision Egg script mode'
            p.parameters.enter_go_loop = False
            p.parameters.quit = False
            p.run_forever()
            if ephys_server.exec_demoscript_flag:
                dropin_meta_params = stimulus_meta_controller.get_parameters()
                ephys_server.exec_AST(screen, dropin_meta_params)
            if ephys_server.get_stimkey() == 'dropin_server':
                loadNewExpr = False
            else:
                pyro_server.disconnect(stimulus_meta_controller)
                del stimulus_meta_controller
                loadNewExpr = True
        else:
            overlay2D_viewport.parameters.stimuli = []
            for stim in stimulus_list:
                if stim[0] == '3d_perspective':
                    perspective_viewport.parameters.stimuli.append(stim[1])
                elif stim[0] == '3d_perspective_with_set_viewport_callback':
                    (key, stimulus, callback_function) = stim
                    callback_function(perspective_viewport)
                    perspective_viewport.parameters.stimuli.append(stimulus)
                elif stim[0] == '2d_overlay':
                    overlay2D_viewport.parameters.stimuli.append(stim[1])
                else:
                    raise RuntimeError('Unknown viewport id %s' % stim[0])

            p.parameters.enter_go_loop = False
            p.parameters.quit = False
            p.run_forever()
            pyro_server.disconnect(stimulus_meta_controller)
            del stimulus_meta_controller

    return


if __name__ == '__main__':
    start_server(server_modules)