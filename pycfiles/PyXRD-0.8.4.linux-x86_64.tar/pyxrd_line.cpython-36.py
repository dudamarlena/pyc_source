# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/models/lines/pyxrd_line.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 13019 bytes
import logging
logger = logging.getLogger(__name__)
import numpy as np
from scipy import stats
from scipy.interpolate import interp1d
from mvc.models.properties import StringProperty, BoolProperty, FloatProperty, StringChoiceProperty, SignalMixin, ListProperty
from pyxrd.data import settings
from pyxrd.generic.utils import not_none
from pyxrd.generic.io.custom_io import storables
from pyxrd.generic.models.properties import InheritableMixin
from pyxrd.calculations.peak_detection import multi_peakdetect
from .storable_xy_data import StorableXYData

@storables.register()
class PyXRDLine(StorableXYData):
    __doc__ = "\n        A PyXRDLine is an abstract attribute holder for a real 'Line' object,\n        whatever the plotting library used may be. Attributes are line width and\n        color.        \n    "

    class Meta(StorableXYData.Meta):
        store_id = 'PyXRDLine'

    label = StringProperty(default='',
      text='Label',
      persistent=True)
    color = StringProperty(default='#000000',
      text='Label',
      visible=True,
      persistent=True,
      widget_type='color',
      inherit_flag='inherit_color',
      inherit_from='parent.parent.display_exp_color',
      signal_name='visuals_changed',
      mix_with=(
     InheritableMixin, SignalMixin))
    inherit_color = BoolProperty(default=True,
      text='Inherit color',
      visible=True,
      persistent=True,
      signal_name='visuals_changed',
      mix_with=(SignalMixin,))
    lw = FloatProperty(default=2.0,
      text='Linewidth',
      visible=True,
      persistent=True,
      widget_type='spin',
      inherit_flag='inherit_lw',
      inherit_from='parent.parent.display_exp_lw',
      signal_name='visuals_changed',
      mix_with=(
     InheritableMixin, SignalMixin))
    inherit_lw = BoolProperty(default=True,
      text='Inherit linewidth',
      visible=True,
      persistent=True,
      signal_name='visuals_changed',
      mix_with=(SignalMixin,))
    ls = StringChoiceProperty(default=(settings.EXPERIMENTAL_LINESTYLE),
      text='Linestyle',
      visible=True,
      persistent=True,
      choices=(settings.PATTERN_LINE_STYLES),
      mix_with=(
     InheritableMixin, SignalMixin),
      signal_name='visuals_changed',
      inherit_flag='inherit_ls',
      inherit_from='parent.parent.display_exp_ls')
    inherit_ls = BoolProperty(default=True,
      text='Inherit linestyle',
      visible=True,
      persistent=True,
      mix_with=(
     SignalMixin,),
      signal_name='visuals_changed')
    marker = StringChoiceProperty(default=(settings.EXPERIMENTAL_MARKER),
      text='Marker',
      visible=True,
      persistent=True,
      choices=(settings.PATTERN_MARKERS),
      mix_with=(
     InheritableMixin, SignalMixin),
      signal_name='visuals_changed',
      inherit_flag='inherit_marker',
      inherit_from='parent.parent.display_exp_marker')
    inherit_marker = BoolProperty(default=True,
      text='Inherit marker',
      visible=True,
      persistent=True,
      mix_with=(
     SignalMixin,),
      signal_name='visuals_changed')
    z_data = ListProperty(default=None,
      text='Z data',
      data_type=float,
      persistent=True,
      visible=False)

    @property
    def max_display_y(self):
        if self.num_columns > 2:
            if len(self.z_data) > 2:
                return np.max(self.z_data)
            else:
                return self.max_y
        else:
            return self.max_y

    @property
    def min_intensity(self):
        if self.num_columns > 2:
            return np.min(self.z_data)
        else:
            return self.min_y

    @property
    def abs_max_intensity(self):
        return self.abs_max_y

    def __init__(self, *args, **kwargs):
        my_kwargs = (self.pop_kwargs)(kwargs, *[prop.label for prop in PyXRDLine.Meta.get_local_persistent_properties()])
        (super(PyXRDLine, self).__init__)(*args, **kwargs)
        kwargs = my_kwargs
        with self.visuals_changed.hold():
            self.label = self.get_kwarg(kwargs, self.label, 'label')
            self.color = self.get_kwarg(kwargs, self.color, 'color')
            self.inherit_color = bool(self.get_kwarg(kwargs, self.inherit_color, 'inherit_color'))
            self.lw = float(self.get_kwarg(kwargs, self.lw, 'lw'))
            self.inherit_lw = bool(self.get_kwarg(kwargs, self.inherit_lw, 'inherit_lw'))
            self.ls = self.get_kwarg(kwargs, self.ls, 'ls')
            self.inherit_ls = bool(self.get_kwarg(kwargs, self.inherit_ls, 'inherit_ls'))
            self.marker = self.get_kwarg(kwargs, self.marker, 'marker')
            self.inherit_marker = bool(self.get_kwarg(kwargs, self.inherit_marker, 'inherit_marker'))
            self.z_data = list(self.get_kwarg(kwargs, [0], 'z_data'))

    @classmethod
    def from_json(cls, **kwargs):
        if 'xy_store' in kwargs:
            if 'type' in kwargs['xy_store']:
                kwargs['data'] = kwargs['xy_store']['properties']['data']
        else:
            if 'xy_data' in kwargs:
                if 'type' in kwargs['xy_data']:
                    kwargs['data'] = kwargs['xy_data']['properties']['data']
                kwargs['label'] = kwargs['data_label']
                del kwargs['data_name']
                del kwargs['data_label']
                del kwargs['xy_data']
        return cls(**kwargs)

    def interpolate(self, *x_vals, **kwargs):
        """
            Returns a list of (x, y) tuples for the passed x values. An optional
            column keyword argument can be passed to select a column, by default
            the first y-column is used. Returned y-values are interpolated. 
        """
        column = kwargs.get('column', 0)
        f = interp1d(self.data_x, self.data_y[:, column])
        return list(zip(x_vals, f(x_vals)))

    def get_plotted_y_at_x(self, x):
        """
            Gets the (interpolated) plotted value at the given x position.
            If this line has not been plotted (or does not have
            access to a '__plot_line' attribute set by the plotting routines)
            it will return 0.
        """
        try:
            xdata, ydata = getattr(self, '__plot_line').get_data()
        except AttributeError:
            logging.exception('Attribute error when trying to get plotter data at x position!')
        else:
            if len(xdata) > 0:
                if len(ydata) > 0:
                    return np.interp(x, xdata, ydata)
            return 0

    def calculate_npeaks_for(self, max_threshold, steps):
        """
            Calculates the number of peaks for `steps` threshold values between
            0 and `max_threshold`. Returns a tuple containing two lists with the
            threshold values and the corresponding number of peaks. 
        """
        length = self.data_x.size
        resolution = length / (self.data_x[(-1)] - self.data_x[0])
        delta_angle = 0.05
        window = int(delta_angle * resolution)
        window += window % 2 * 2
        steps = max(steps, 2) - 1
        factor = max_threshold / steps
        deltas = [i * factor for i in range(0, steps)]
        numpeaks = []
        maxtabs, mintabs = multi_peakdetect(self.data_y[:, 0], self.data_x, 5, deltas)
        for maxtab, _ in zip(maxtabs, mintabs):
            numpeak = len(maxtab)
            numpeaks.append(numpeak)

        numpeaks = list(map(float, numpeaks))
        return (
         deltas, numpeaks)

    def get_best_threshold(self, max_threshold=None, steps=None, status_dict=None):
        """
            Estimates the best threshold for peak detection using an
            iterative algorithm. Assumes there is a linear contribution from noise.
            Returns a 4-tuple containing the selected threshold, the maximum
            threshold, a list of threshold values and a list with the corresponding
            number of peaks.
        """
        length = self.data_x.size
        steps = not_none(steps, 20)
        threshold = 0.1
        max_threshold = not_none(max_threshold, threshold * 3.2)

        def get_new_threshold(threshold, deltas, num_peaks, ln):
            x = deltas[:ln]
            y = num_peaks[:ln]
            slope, intercept, R, _, _ = stats.linregress(x, y)
            return (R, -intercept / slope)

        if length > 2:
            deltas, num_peaks = self.calculate_npeaks_for(max_threshold, steps)
            last_threshold = None
            solution = False
            max_iters = 10
            min_iters = 3
            itercount = 0
            if status_dict is not None:
                status_dict['progress'] = 0
            while not solution:
                ln = 4
                max_ln = len(deltas)
                stop = False
                while not stop:
                    R, threshold = get_new_threshold(threshold, deltas, num_peaks, ln)
                    max_threshold = threshold * 3.2
                    if abs(R) < 0.98 or ln >= max_ln:
                        stop = True
                    else:
                        ln += 1

                itercount += 1
                if last_threshold:
                    solution = bool(itercount > min_iters and not (itercount <= max_iters and last_threshold - threshold >= 0.001))
                    if not solution:
                        deltas, num_peaks = self.calculate_npeaks_for(max_threshold, steps)
                last_threshold = threshold
                if status_dict is not None:
                    status_dict['progress'] = float(itercount / max_iters)

            return ((deltas, num_peaks), threshold, max_threshold)
        else:
            return (([], []), threshold, max_threshold)