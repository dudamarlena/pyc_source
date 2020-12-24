# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/controllers/line_controllers.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 10640 bytes
import os
from mvc.adapters.gtk_support.dialogs.dialog_factory import DialogFactory
from pyxrd.generic.controllers import BaseController, DialogController
from pyxrd.generic.plot.eye_dropper import EyeDropper
from pyxrd.file_parsers.xrd_parsers import xrd_parsers
from pyxrd.data import settings

class LinePropertiesController(BaseController):
    __doc__ = "\n        Controller for Line models' general properties\n    "
    auto_adapt_excluded = [
     'noise_fraction',
     'shift_value',
     'shift_position',
     'smooth_type',
     'smooth_degree',
     'strip_startx',
     'strip_endx',
     'noise_level',
     'bg_type',
     'bg_position',
     'bg_scale',
     'peak_startx',
     'peak_endx',
     'peak_area_result',
     'peak_fwhm_result']
    __LINEID__ = 'TRUE'

    def register_adapters(self):
        super(LinePropertiesController, self).register_adapters()
        self.update_sensitivities()

    def update_sensitivities(self):
        """
            Updates the views sensitivities according to the model state.
        """
        self.view[(self.view.widget_format % 'color')].set_sensitive(not self.model.inherit_color)
        self.view[('spb_%s' % self.view.widget_format % 'lw')].set_sensitive(not self.model.inherit_lw)
        self.view[(self.view.widget_format % 'ls')].set_sensitive(not self.model.inherit_ls)
        self.view[(self.view.widget_format % 'marker')].set_sensitive(not self.model.inherit_marker)

    @BaseController.observe('inherit_color', assign=True)
    @BaseController.observe('inherit_lw', assign=True)
    @BaseController.observe('inherit_ls', assign=True)
    @BaseController.observe('inherit_marker', assign=True)
    def notif_color_toggled(self, model, prop_name, info):
        self.update_sensitivities()


class PatternActionController(DialogController):
    __doc__ = '\n        General class for actions that can be applied on ExperimentalPattern\n        models.\n        \n        Attributes:\n         model_setup_method: the name of the method to call on the model to\n          auto-setup any variables for the action. Optional; can be None.\n        model_action_method: the name of the method to call on the model when\n         the user decides to apply the action. Required, cannot be None.\n        model_cancel_method: the name of the method to call on the model when\n         the user decides to cancel the action. Optional; can be None.\n    '
    model_setup_method = None
    model_action_method = None
    model_cancel_method = None

    def register_adapters(self):
        if self.model_setup_method is not None:
            getattr(self.model, self.model_setup_method)()
        return super(PatternActionController, self).register_adapters()

    def on_btn_ok_clicked(self, event):
        try:
            action = getattr(self.model, self.model_action_method)
        except AttributeError:
            raise ValueError("Subclasses of PatternActionController should specify a valid action method name (was '%s')!" % self.model_action_method)
        else:
            action()
        return super(PatternActionController, self).on_btn_ok_clicked(event)

    def on_cancel(self):
        if self.model_cancel_method is not None:
            getattr(self.model, self.model_cancel_method)()
        return super(PatternActionController, self).on_cancel()


class AddNoiseController(PatternActionController):
    __doc__ = "\n        Controller for the experimental pattern 'add noise' action view.\n    "
    auto_adapt_included = [
     'noise_fraction']
    model_setup_method = None
    model_action_method = 'add_noise'
    model_cancel_method = 'clear_noise_variables'


class ShiftDataController(PatternActionController):
    __doc__ = "\n        Controller for the experimental pattern 'shift data' action view.\n    "
    auto_adapt_included = [
     'shift_value',
     'shift_position']
    model_setup_method = 'setup_shift_variables'
    model_action_method = 'shift_data'
    model_cancel_method = 'clear_shift_variables'


class SmoothDataController(PatternActionController):
    auto_adapt_included = [
     'smooth_type',
     'smooth_degree']
    model_setup_method = 'setup_smooth_variables'
    model_action_method = 'smooth_data'
    model_cancel_method = 'clear_smooth_variables'


class CalculatePeakPropertiesController(PatternActionController):
    auto_adapt_included = [
     'peak_startx',
     'peak_endx',
     'peak_fwhm_result',
     'peak_area_result']
    model_setup_method = None
    model_action_method = 'clear_peak_properties_variables'
    model_cancel_method = 'clear_peak_properties_variables'

    def on_sample_start_clicked(self, event):
        self.sample('peak_startx')
        return True

    def on_sample_end_clicked(self, event):
        self.sample('peak_endx')
        return True

    def sample(self, attribute):

        def onclick(x_pos, *args):
            if self.edc is not None:
                self.edc.enabled = False
                self.edc.disconnect()
                self.edc = None
            if x_pos != -1:
                setattr(self.model, attribute, x_pos)
            self.view.get_toplevel().present()

        self.edc = EyeDropper(self.parent.parent.plot_controller, onclick)
        self.view.get_toplevel().hide()
        self.parent.parent.view.get_toplevel().present()


class StripPeakController(PatternActionController):
    auto_adapt_included = [
     'strip_startx',
     'strip_endx',
     'noise_level']
    model_setup_method = None
    model_action_method = 'strip_peak'
    model_cancel_method = 'clear_strip_variables'

    def on_sample_start_clicked(self, event):
        self.sample('strip_startx')
        return True

    def on_sample_end_clicked(self, event):
        self.sample('strip_endx')
        return True

    def sample(self, attribute):

        def onclick(x_pos, *args):
            if self.edc is not None:
                self.edc.enabled = False
                self.edc.disconnect()
                self.edc = None
            if x_pos != -1:
                setattr(self.model, attribute, x_pos)
            self.view.get_toplevel().present()

        self.edc = EyeDropper(self.parent.parent.plot_controller, onclick)
        self.view.get_toplevel().hide()
        self.parent.parent.view.get_toplevel().present()


class BackgroundController(PatternActionController):
    __doc__ = "\n        Controller for the experimental pattern 'remove background' action view.\n    "
    file_filters = xrd_parsers.get_import_file_filters()
    auto_adapt_included = [
     'bg_type',
     'bg_position',
     'bg_scale']
    model_setup_method = 'find_bg_position'
    model_action_method = 'remove_background'
    model_cancel_method = 'clear_bg_variables'

    def register_view(self, view):
        super(BackgroundController, self).register_view(view)
        view.set_file_dialog(DialogFactory.get_load_dialog(title='Open XRD file for import',
          parent=(view.get_top_widget()),
          filters=(self.file_filters)), self.on_pattern_file_set)
        view.select_bg_view(self.model.get_bg_type_lbl().lower())

    @PatternActionController.observe('bg_type', assign=True)
    def notif_bg_type_changed(self, model, prop_name, info):
        self.view.select_bg_view(self.model.get_bg_type_lbl().lower())

    def on_pattern_file_set(self, button, dialog):
        filename = dialog.filename
        parser = dialog.parser
        data_objects = None
        message = 'An unexpected error has occurred when trying to parse %s:\n\n<i>' % os.path.basename(filename)
        message += '{}</i>\n\n'
        message += 'This is most likely caused by an invalid or unsupported file format.'
        with DialogFactory.error_dialog_handler(message, parent=(self.view.get_toplevel()), reraise=(settings.DEBUG)):
            data_objects = parser.parse(filename)
            pattern = data_objects[0].data
            bg_pattern_x = pattern[:, 0].copy()
            bg_pattern_y = pattern[:, 1].copy()
            del pattern
            from scipy.interpolate import interp1d
            f = interp1d(bg_pattern_x,
              bg_pattern_y, bounds_error=False,
              fill_value=0)
            bg_xnew = self.model.data_x
            bg_ynew = f(bg_xnew)
            self.model.bg_pattern = bg_ynew