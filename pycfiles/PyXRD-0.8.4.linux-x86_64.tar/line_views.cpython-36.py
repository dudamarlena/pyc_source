# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/views/line_views.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2885 bytes
from pkg_resources import resource_filename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pyxrd.generic.views import DialogView, BaseView

class CalculatedLinePropertiesView(BaseView):
    builder = resource_filename(__name__, 'glade/lines/calculated_props.glade')
    top = 'cal_line_props'
    widget_format = 'cal_%s'
    widget_groups = {'full_mode_only': [
                        'cal_line_props']}


class ExperimentalLinePropertiesView(BaseView):
    builder = resource_filename(__name__, 'glade/lines/experimental_props.glade')
    top = 'exp_line_props'
    widget_format = 'exp_%s'


class BackgroundView(DialogView):
    title = 'Remove Background'
    subview_builder = resource_filename(__name__, 'glade/lines/background.glade')
    subview_toplevel = 'edit_background'
    modal = True
    resizable = False
    def_bg_view = 'bg_linear'
    bg_view_cont = 'bg_view_container'

    def select_bg_view(self, bg_view=None):
        if bg_view is not None:
            bg_view = 'bg_%s' % bg_view
        else:
            bg_view = self.def_bg_view
        self._add_child_view(self[bg_view], self[self.bg_view_cont])

    def set_file_dialog(self, dialog, callback):
        fcb_bg_pattern = Gtk.FileChooserButton(dialog)
        fcb_bg_pattern.connect('file-set', callback, dialog)
        self['fcb_bg_container'].add(fcb_bg_pattern)


class AddNoiseView(DialogView):
    title = 'Add Noise'
    subview_builder = resource_filename(__name__, 'glade/lines/add_noise.glade')
    subview_toplevel = 'add_noise'
    modal = True
    resizable = False


class SmoothDataView(DialogView):
    title = 'Smooth Data'
    subview_builder = resource_filename(__name__, 'glade/lines/smoothing.glade')
    subview_toplevel = 'smooth_data'
    modal = True
    resizable = False


class ShiftDataView(DialogView):
    title = 'Shift Pattern'
    subview_builder = resource_filename(__name__, 'glade/lines/shifting.glade')
    subview_toplevel = 'shift_pattern'
    modal = True
    resizable = False


class StripPeakView(DialogView):
    title = 'Strip Peak'
    subview_builder = resource_filename(__name__, 'glade/lines/strip_peak.glade')
    subview_toplevel = 'strip_peak'
    modal = True
    resizable = False


class CalculatePeakPropertiesView(DialogView):
    title = 'Calculate Peak Properties'
    subview_builder = resource_filename(__name__, 'glade/lines/peak_properties.glade')
    subview_toplevel = 'peak_properties'
    modal = True
    resizable = False