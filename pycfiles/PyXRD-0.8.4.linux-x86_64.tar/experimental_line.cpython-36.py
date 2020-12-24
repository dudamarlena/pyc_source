# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/models/lines/experimental_line.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 18243 bytes
import logging
logger = logging.getLogger(__name__)
import numpy as np
from scipy.integrate import trapz
from scipy.interpolate import UnivariateSpline
from mvc.models.properties.tools import modify
from mvc.models.properties import FloatProperty, LabeledProperty, IntegerProperty, FloatChoiceProperty, IntegerChoiceProperty, SetActionMixin, SignalMixin
from pyxrd.data import settings
from pyxrd.generic.io import storables
from pyxrd.calculations.math_tools import smooth, add_noise
from pyxrd.generic.models.base import DataModel
from .pyxrd_line import PyXRDLine

@storables.register()
class ExperimentalLine(PyXRDLine):

    class Meta(PyXRDLine.Meta):
        store_id = 'ExperimentalLine'

    specimen = property(DataModel.parent.fget, DataModel.parent.fset)
    color = modify((PyXRDLine.color), default=(settings.EXPERIMENTAL_COLOR),
      inherit_from='parent.parent.display_exp_color')
    lw = modify((PyXRDLine.lw), default=(settings.EXPERIMENTAL_LINEWIDTH),
      inherit_from='parent.parent.display_exp_lw')
    ls = modify((PyXRDLine.ls), default=(settings.EXPERIMENTAL_LINESTYLE),
      inherit_from='parent.parent.display_exp_ls')
    marker = modify((PyXRDLine.marker), default=(settings.EXPERIMENTAL_MARKER),
      inherit_from='parent.parent.display_exp_marker')
    cap_value = FloatProperty(default=0.0,
      text='Cap value',
      persistent=True,
      visible=True,
      widget_type='float_entry',
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))

    @property
    def max_display_y(self):
        max_value = super(ExperimentalLine, self).max_display_y
        if self.cap_value > 0:
            if not (self.num_columns > 2 and len(self.z_data)):
                max_value = min(max_value, self.cap_value)
        return max_value

    bg_position = FloatProperty(default=0.0,
      text='Background offset',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    bg_scale = FloatProperty(default=1.0,
      text='Background scale',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    bg_pattern = LabeledProperty(default=None,
      text='Background pattern',
      persistent=False,
      visible=False,
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    bg_type = IntegerChoiceProperty(default=0,
      text='Background type',
      choices=(settings.PATTERN_BG_TYPES),
      persistent=False,
      visible=True,
      signal_name='visuals_changed',
      set_action_name='find_bg_position',
      mix_with=(
     SignalMixin, SetActionMixin))

    def get_bg_type_lbl(self):
        return settings.PATTERN_BG_TYPES[self.bg_type]

    smooth_type = IntegerChoiceProperty(default=0,
      text='Smooth type',
      choices=(settings.PATTERN_SMOOTH_TYPES),
      persistent=False,
      visible=True,
      signal_name='visuals_changed',
      set_action_name='setup_smooth_variables',
      mix_with=(
     SignalMixin, SetActionMixin))
    smooth_pattern = None
    smooth_degree = IntegerProperty(default=0,
      text='Smooth degree',
      persistent=False,
      visible=True,
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    noise_fraction = FloatProperty(default=0.0,
      text='Noise fraction',
      persistent=False,
      visible=True,
      widget_type='spin',
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    shift_value = FloatProperty(default=0.0,
      text='Shift value',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    shift_position = FloatChoiceProperty(default=0.42574,
      text='Shift position',
      choices=(settings.PATTERN_SHIFT_POSITIONS),
      persistent=False,
      visible=True,
      signal_name='visuals_changed',
      set_action_name='setup_shift_variables',
      mix_with=(
     SignalMixin, SetActionMixin))
    peak_startx = FloatProperty(default=0.0,
      text='Peak properties start position',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      set_action_name='update_peak_properties',
      mix_with=(
     SetActionMixin,))
    peak_endx = FloatProperty(default=0.0,
      text='Peak properties end position',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      set_action_name='update_peak_properties',
      mix_with=(
     SetActionMixin,))
    peak_fwhm_result = FloatProperty(default=0.0,
      text='Peak FWHM value',
      persistent=False,
      visible=True,
      widget_type='label')
    peak_area_result = FloatProperty(default=0.0,
      text='Peak area value',
      persistent=False,
      visible=True,
      widget_type='label')
    peak_properties_pattern = LabeledProperty(default=None,
      text='Peak properties pattern',
      persistent=False,
      visible=False,
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    strip_startx = FloatProperty(default=0.0,
      text='Strip peak start position',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      set_action_name='update_strip_pattern',
      mix_with=(
     SetActionMixin,))
    strip_endx = FloatProperty(default=0.0,
      text='Strip peak end position',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      set_action_name='update_strip_pattern',
      mix_with=(
     SetActionMixin,))
    stripped_pattern = LabeledProperty(default=None,
      text='Strip peak pattern',
      persistent=False,
      visible=False,
      signal_name='visuals_changed',
      mix_with=(
     SignalMixin,))
    noise_level = FloatProperty(default=0.0,
      text='Strip peak noise level',
      persistent=False,
      visible=True,
      widget_type='float_entry',
      set_action_name='update_strip_pattern_noise',
      mix_with=(
     SetActionMixin,))

    def __init__(self, cap_value=0.0, *args, **kwargs):
        """
            Valid keyword arguments for a ExperimentalLine are:
                cap_value: the value (in raw counts) at which to cap
                 the experimental pattern  
        """
        (super(ExperimentalLine, self).__init__)(*args, **kwargs)
        self.cap_value = cap_value

    def remove_background(self):
        with self.data_changed.hold_and_emit():
            bg = None
            if self.bg_type == 0:
                bg = self.bg_position
            else:
                if self.bg_type == 1:
                    if self.bg_pattern is not None:
                        if not (self.bg_position == 0 and self.bg_scale == 0):
                            bg = self.bg_pattern * self.bg_scale + self.bg_position
            if bg is not None:
                if self.data_y.size > 0:
                    self.data_y[:, 0] -= bg
            self.clear_bg_variables()

    def find_bg_position(self):
        try:
            self.bg_position = np.min(self.data_y)
        except ValueError:
            return 0.0

    def clear_bg_variables(self):
        with self.visuals_changed.hold_and_emit():
            self.bg_pattern = None
            self.bg_scale = 0.0
            self.bg_position = 0.0

    def smooth_data(self):
        with self.data_changed.hold_and_emit():
            if self.smooth_degree > 0:
                degree = int(self.smooth_degree)
                self.data_y[:, 0] = smooth(self.data_y[:, 0], degree)
            self.smooth_degree = 0.0

    def setup_smooth_variables(self):
        with self.visuals_changed.hold_and_emit():
            self.smooth_degree = 5.0

    def clear_smooth_variables(self):
        with self.visuals_changed.hold_and_emit():
            self.smooth_degree = 0.0

    def add_noise(self):
        with self.data_changed.hold_and_emit():
            if self.noise_fraction > 0:
                noisified = add_noise(self.data_y[:, 0], self.noise_fraction)
                self.set_data(self.data_x, noisified)
            self.noise_fraction = 0.0

    def clear_noise_variables(self):
        with self.visuals_changed.hold_and_emit():
            self.noise_fraction = 0.0

    def shift_data(self):
        with self.data_changed.hold_and_emit():
            if self.shift_value != 0.0:
                if settings.PATTERN_SHIFT_TYPE == 'Linear':
                    self.data_x = self.data_x - self.shift_value
                    if self.specimen is not None:
                        with self.specimen.visuals_changed.hold():
                            for marker in self.specimen.markers:
                                marker.position = marker.position - self.shift_value

                elif settings.PATTERN_SHIFT_TYPE == 'Displacement':
                    position = self.specimen.goniometer.get_t_from_nm(self.shift_position)
                    displacement = 0.5 * self.specimen.goniometer.radius * self.shift_value / np.cos(position / 180 * np.pi)
                    correction = 2 * displacement * np.cos(self.data_x / 2 / 180 * np.pi) / self.specimen.goniometer.radius
                    self.data_x = self.data_x - correction
            self.shift_value = 0.0

    def setup_shift_variables(self):
        with self.visuals_changed.hold_and_emit():
            position = self.specimen.goniometer.get_2t_from_nm(self.shift_position)
            if position > 0.1:
                max_x = position + 0.5
                min_x = position - 0.5
                condition = (self.data_x >= min_x) & (self.data_x <= max_x)
                section_x, section_y = np.extract(condition, self.data_x), np.extract(condition, self.data_y[:, 0])
                try:
                    actual_position = section_x[np.argmax(section_y)]
                except ValueError:
                    actual_position = position

                self.shift_value = actual_position - position

    def clear_shift_variables(self):
        with self.visuals_changed.hold_and_emit():
            self.shift_value = 0

    peak_bg_slope = 0.0
    avg_starty = 0.0
    avg_endy = 0.0

    def update_peak_properties(self):
        with self.visuals_changed.hold_and_emit():
            if self.peak_endx < self.peak_startx:
                self.peak_endx = self.peak_startx + 1.0
                return
            condition = (self.data_x >= self.peak_startx - 0.1) & (self.data_x <= self.peak_startx + 0.1)
            section = np.extract(condition, self.data_y[:, 0])
            self.avg_starty = np.min(section)
            condition = (self.data_x >= self.peak_endx - 0.1) & (self.data_x <= self.peak_endx + 0.1)
            section = np.extract(condition, self.data_y[:, 0])
            self.avg_endy = np.min(section)
            self.peak_bg_slope = (self.avg_starty - self.avg_endy) / (self.peak_startx - self.peak_endx)
            condition = (self.data_x >= self.peak_startx) & (self.data_x <= self.peak_endx)
            section_x = np.extract(condition, self.data_x)
            section_y = np.extract(condition, self.data_y)
            bg_curve = self.peak_bg_slope * (section_x - self.peak_startx) + self.avg_starty
            self.peak_area_result = abs(trapz(section_y, x=section_x) - trapz(bg_curve, x=section_x))
            fwhm_curve = section_y - bg_curve
            peak_half_max = np.max(fwhm_curve) * 0.5
            spline = UnivariateSpline(section_x, (fwhm_curve - peak_half_max), s=0)
            roots = spline.roots()
            self.peak_fwhm_result = np.abs(roots[0] - roots[(-1)]) if len(roots) >= 2 else 0
            self.peak_properties_pattern = (
             section_x, bg_curve, section_y, roots, spline(roots) + peak_half_max)

    def clear_peak_properties_variables(self):
        with self.visuals_changed.hold_and_emit():
            self._peak_startx = 0.0
            self._peak_properties_pattern = None
            self._peak_endx = 0.0
            self.peak_properties = 0.0

    def strip_peak(self):
        with self.data_changed.hold_and_emit():
            if self.stripped_pattern is not None:
                stripx, stripy = self.stripped_pattern
                indeces = ((self.data_x >= self.strip_startx) & (self.data_x <= self.strip_endx)).nonzero()[0]
                np.put(self.data_y[:, 0], indeces, stripy)
            self._strip_startx = 0.0
            self._stripped_pattern = None
            self.strip_endx = 0.0

    strip_slope = 0.0
    avg_starty = 0.0
    avg_endy = 0.0
    block_strip = False

    def update_strip_pattern_noise(self):
        with self.visuals_changed.hold_and_emit():
            condition = (self.data_x >= self.strip_startx) & (self.data_x <= self.strip_endx)
            section_x = np.extract(condition, self.data_x)
            noise = self.avg_endy * 2 * ((np.random.rand)(*section_x.shape) - 0.5) * self.noise_level
            section_y = self.strip_slope * (section_x - self.strip_startx) + self.avg_starty + noise
            self.stripped_pattern = (section_x, section_y)

    def update_strip_pattern(self):
        with self.visuals_changed.hold_and_emit():
            if self.strip_endx < self.strip_startx:
                self.strip_endx = self.strip_startx + 1.0
                return
            if not self.block_strip:
                self.block_strip = True
                condition = (self.data_x >= self.strip_startx - 0.1) & (self.data_x <= self.strip_startx + 0.1)
                section = np.extract(condition, self.data_y[:, 0])
                self.avg_starty = np.average(section)
                noise_starty = 2 * np.std(section) / self.avg_starty
                condition = (self.data_x >= self.strip_endx - 0.1) & (self.data_x <= self.strip_endx + 0.1)
                section = np.extract(condition, self.data_y[:, 0])
                self.avg_endy = np.average(section)
                noise_endy = 2 * np.std(section) / self.avg_starty
                self.strip_slope = (self.avg_starty - self.avg_endy) / (self.strip_startx - self.strip_endx)
                self.noise_level = (noise_starty + noise_endy) * 0.5
                self.update_strip_pattern_noise()

    def clear_strip_variables(self):
        with self.visuals_changed.hold_and_emit():
            self._strip_startx = 0.0
            self._strip_pattern = None
            self.strip_start_x = 0.0