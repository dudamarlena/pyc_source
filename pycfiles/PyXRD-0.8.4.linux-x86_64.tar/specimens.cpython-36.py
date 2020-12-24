# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/specimen/views/specimens.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 3038 bytes
from pkg_resources import resource_filename
from pyxrd.generic.views import DialogView, BaseView, HasChildView
from pyxrd.goniometer.views import InlineGoniometerView
from pyxrd.generic.views.line_views import CalculatedLinePropertiesView, ExperimentalLinePropertiesView

class SpecimenView(DialogView, HasChildView):
    title = 'Edit Specimen'
    subview_builder = resource_filename(__name__, '../glade/specimen.glade')
    subview_toplevel = 'edit_specimen'
    resizable = False
    widget_format = 'specimen_%s'
    widget_groups = {'full_mode_only': [
                        'specimen_display_calculated',
                        'specimen_display_stats_in_lbl',
                        'specimen_display_phases',
                        'vbox_calculated_data_tv',
                        'lbl_specimen_calculated',
                        'vbox_exclusion_ranges_tv',
                        'lbl_tabexclusions',
                        'general_separator',
                        'specimen_display_residuals',
                        'specimen_display_derivatives']}
    gonio_container = widget_format % 'goniometer'
    gonio_view = None
    calc_line_container = widget_format % 'calc_line'
    calc_line_view = None
    exp_line_container = widget_format % 'exp_line'
    exp_line_view = None

    def __init__(self, *args, **kwargs):
        (super(SpecimenView, self).__init__)(*args, **kwargs)
        self._init_child_views()
        self._add_child_views()

    _children_ready = False

    def _init_child_views(self):
        if not self._children_ready:
            self.gonio_view = InlineGoniometerView(parent=self)
            self.calc_line_view = CalculatedLinePropertiesView(parent=self)
            self.exp_line_view = ExperimentalLinePropertiesView(parent=self)
            self._children_ready = True

    def _add_child_views(self):
        self._init_child_views()
        top = self.gonio_view.get_top_widget()
        self._add_child_view(top, self[self.gonio_container])
        top = self.calc_line_view.get_top_widget()
        self._add_child_view(top, self[self.calc_line_container])
        top = self.exp_line_view.get_top_widget()
        self._add_child_view(top, self[self.exp_line_container])

    def set_layout_mode(self, state):
        super(SpecimenView, self).set_layout_mode(state)
        if self._children_ready:
            self.gonio_view.set_layout_mode(state)
            self.calc_line_view.set_layout_mode(state)
            self.exp_line_view.set_layout_mode(state)


class StatisticsView(BaseView):
    builder = resource_filename(__name__, '../specimen/glade/statistics.glade')
    top = 'statistics_box'

    def __init__(self, *args, **kwargs):
        (BaseView.__init__)(self, *args, **kwargs)