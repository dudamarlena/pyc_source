# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\DropinGUI.py
# Compiled at: 2009-07-07 11:29:42
import VisionEgg, string, sys, os, Tkinter, tkMessageBox, VisionEgg.PyroApps.VarTypes as VarTypes, VisionEgg.PyroApps.EPhysGUIUtils as client_utils

def get_control_list():
    return [
     (
      'dropin_server', DropinControlFrame, DropinControlFrame.title)]


class DropinMetaParameters:

    def __init__(self):
        self.vars_list = []


class DropinControlFrame(client_utils.StimulusControlFrame):
    title = 'Vision Egg Script'

    def __init__(self, master=None, suppress_go_buttons=0, **kw):
        client_utils.StimulusControlFrame.__init__(self, master, suppress_go_buttons, DropinControlFrame.title, DropinMetaParameters, **kw)
        param_frame = self.param_frame
        param_frame.columnconfigure(0, weight=1)
        param_frame.columnconfigure(1, weight=1)
        self.vars_list = []
        self.error_names = []

    def get_shortname(self):
        return 'dropin'

    def update_tk_vars(self):
        pass

    def send_values(self, dummy_arg=None):
        self.meta_params.vars_list = []
        self.error_names = []
        if self.vars_list is None:
            return 0
        for var in self.vars_list:
            if len(var) == 3:
                var_type = var[0]
                var_name = var[1]
                var_val_holder = var[2]
                var_val = var_val_holder.get()
                try:
                    if var_val == 'compound':
                        pass
                    else:
                        if VarTypes.getType(var_type) == 'float':
                            var_typed_val = float(var_val)
                        elif VarTypes.getType(var_type) == 'integer':
                            var_typed_val = int(float(var_val))
                        elif VarTypes.getType(var_type) == 'string':
                            var_typed_val = var_val
                        else:
                            raise ValueError()
                        self.meta_params.vars_list.append([var_name, var_typed_val])
                except ValueError:
                    self.error_names.append(var_name)

        if len(self.error_names) == 0:
            self.meta_controller.set_parameters(self.meta_params)
            return 1
        else:
            all_error_names = 'Invalid value(s) for the following variable(s):\n'
            for error_name in self.error_names:
                all_error_names = all_error_names + error_name + '\n'

            tkMessageBox.showerror('Invalid value(s)', all_error_names)
            return 0
        return

    def get_duration_sec(self):
        return -1

    def gen_var_widgets(self, demoscript_filename, vars_list):
        self.vars_list = vars_list
        param_frame = self.param_frame
        if demoscript_filename is None:
            label = 'No demo file loaded'
        else:
            label = demoscript_filename
        Tkinter.Label(param_frame, text=label, font=('Helvetica', 8, 'bold')).grid(row=0, columnspan=2)
        row_num = 1
        if self.vars_list is None:
            return
        for var in self.vars_list:
            var_label = Tkinter.Label(param_frame, text=var[1]).grid(row=row_num, column=0)
            var_val_holder = Tkinter.StringVar()
            var_val_holder.set(var[2])
            if var[2] == 'not found':
                self.make_callback_entry(textvariable=var_val_holder, state='disabled').grid(row=row_num, column=1)
                del var[2]
            else:
                self.make_callback_entry(textvariable=var_val_holder).grid(row=row_num, column=1)
                var[2] = var_val_holder
            row_num = row_num + 1

        return


if __name__ == '__main__':
    frame = DropinControlFrame()
    frame.pack(expand=1, fill=Tkinter.BOTH)
    frame.winfo_toplevel().title('%s' % (os.path.basename(os.path.splitext(sys.argv[0])[0]),))
    frame.mainloop()