# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\GridGUI.py
# Compiled at: 2009-07-15 18:56:28
import VisionEgg, string, sys, os, Tkinter, VisionEgg.PyroApps.EPhysGUIUtils as client_utils

def get_control_list():
    return [
     (
      'grid_server', GridControlFrame, GridControlFrame.title)]


class GridMetaParameters:

    def __init__(self):
        pass


class GridControlFrame(client_utils.StimulusControlFrame):
    title = 'Grid for 3D calibration'

    def __init__(self, master=None, suppress_go_buttons=0, **kw):
        client_utils.StimulusControlFrame.__init__(self, master, suppress_go_buttons, GridControlFrame.title, GridMetaParameters, **kw)
        Tkinter.Label(self.param_frame, text='No variables to control').grid()

    def get_shortname(self):
        """Used as basename for saving parameter files"""
        return 'grid'

    def update_tk_vars(self):
        pass

    def send_values(self, dummy_arg=None):
        if self.connected:
            self.meta_controller.set_parameters(self.meta_params)

    def get_duration_sec(self):
        return 0.0


if __name__ == '__main__':
    frame = GridControlFrame()
    frame.pack(expand=1, fill=Tkinter.BOTH)
    frame.winfo_toplevel().title('%s' % (os.path.basename(os.path.splitext(sys.argv[0])[0]),))
    frame.mainloop()