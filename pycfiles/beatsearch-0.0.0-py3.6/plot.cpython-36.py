# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\beatsearch\plot.py
# Compiled at: 2018-03-19 11:55:51
# Size of source mod 2**32: 20381 bytes
import math, enum, numpy as np, typing as tp, matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import to_rgba
from matplotlib.patches import Wedge
from abc import ABCMeta, abstractmethod
from itertools import cycle, repeat
from beatsearch.rhythm import Unit, RhythmLoop, Rhythm, Track
from beatsearch.feature_extraction import IOIVector, BinarySchillingerChain, RhythmFeatureExtractorBase, ChronotonicChain, OnsetPositionVector, IOIHistogram
from beatsearch.utils import Quantizable
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

class SnapsToGridPolicy(enum.Enum):
    ALWAYS = enum.auto()
    NEVER = enum.auto()
    ADJUSTABLE = enum.auto()
    NOT_APPLICABLE = enum.auto()


def get_coordinates_on_circle(circle_position, circle_radius, x):
    x *= 2.0
    p_x = circle_radius * math.sin(x * math.pi) + circle_position[0]
    p_y = circle_radius * math.cos(x * math.pi) + circle_position[1]
    return (p_x, p_y)


def to_concrete_unit(unit, rhythm):
    if unit == 'ticks':
        return rhythm.get_resolution()
    else:
        return unit


def plot_rhythm_grid(axes: plt.Axes, rhythm: Rhythm, unit, axis='x'):
    duration = rhythm.get_duration(unit)
    measure_duration = rhythm.get_measure_duration(unit)
    beat_duration = rhythm.get_beat_duration(unit)
    measure_grid_ticks = np.arange(0, duration + 1, measure_duration)
    beat_grid_ticks = np.arange(0, duration + 1, beat_duration)
    if len(axis) > 2:
        raise ValueError('Illegal axis: %s' % axis)
    axes.set_xticks(measure_grid_ticks)
    axes.set_xticks(beat_grid_ticks, minor=True)
    axes.set_yticks(measure_grid_ticks)
    axes.set_yticks(beat_grid_ticks, minor=True)
    axes.set_axisbelow(True)
    axes.grid(which='minor', alpha=0.2, axis=axis)
    axes.grid(which='major', alpha=0.5, axis=axis)


class Orientation(enum.Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class SubplotLayout(object, metaclass=ABCMeta):

    def __init__(self, share_axis=None):
        self.share_x, self.share_y = self.parse_axis_arg_str(share_axis)

    @abstractmethod
    def inflate(self, figure: plt.Figure, n_subplots: int, subplot_kwargs: tp.Dict[(str, tp.Any)]) -> tp.Iterable[plt.Axes]:
        """
        Should create and add subplots to the given figure and return the subplot axes. Implementations of this method
        should pay attention to the share_x and share_y attributes and link the axes of the subplots accordingly.

        :param figure: figure to add the subplots to
        :param n_subplots: subplot count
        :param subplot_kwargs: named arguments to pass to the figure.add_subplot method
        :return: iterable of axes
        """
        raise NotImplementedError

    @staticmethod
    def parse_axis_arg_str(axis_arg_str):
        axis_arg_options = {None:(False, False), 
         'both':(False, False), 
         'x':(True, False), 
         'y':(False, True)}
        try:
            return axis_arg_options[axis_arg_str]
        except KeyError:
            raise ValueError("Unknown axis '%s', choose between %s" % (axis_arg_str, list(axis_arg_options.keys())))


class CombinedSubplotLayout(SubplotLayout):

    def inflate(self, figure: plt.Figure, n_subplots: int, subplot_kwargs: tp.Dict[(str, tp.Any)]) -> tp.Iterable[plt.Axes]:
        axes = (figure.add_subplot)(*(111, ), **subplot_kwargs)
        return repeat(axes, n_subplots)


class StackedSubplotLayout(SubplotLayout):
    _StackedSubplotLayout__subplot_args_by_orientation = {Orientation.HORIZONTAL: lambda n, i: [1, n, i + 1], 
     Orientation.VERTICAL: lambda n, i: [n, 1, i + 1]}

    def __init__(self, orientation=Orientation.VERTICAL, share_axis='both'):
        super().__init__(share_axis)
        self.check_orientation(orientation)
        self._orientation = orientation

    def inflate(self, figure: plt.Figure, n_subplots: int, subplot_kwargs: tp.Dict[(str, tp.Any)]) -> tp.Iterable[plt.Axes]:
        orientation = self._orientation
        get_subplot_positional_args = self._StackedSubplotLayout__subplot_args_by_orientation[orientation]
        prev_subplot = None
        for subplot_ix in range(n_subplots):
            subplot_positional_args = get_subplot_positional_args(n_subplots, subplot_ix)
            subplot = (figure.add_subplot)(*subplot_positional_args, **{**subplot_kwargs, **{'sharex':prev_subplot if self.share_x else None, 
              'sharey':prev_subplot if self.share_y else None}})
            yield subplot
            prev_subplot = subplot

    @classmethod
    def check_orientation(cls, orientation: Orientation):
        if orientation not in cls._StackedSubplotLayout__subplot_args_by_orientation:
            raise ValueError('Unknown orientation: %s' % str(orientation))


class RhythmLoopPlotter(object, metaclass=ABCMeta):
    COLORS = [
     '#d53e4f', '#fc8d59', '#fee08b', '#e6f598', '#99d594', '#3288bd']

    def __init__(self, unit: str, subplot_layout: SubplotLayout, feature_extractors: tp.Optional[tp.Dict[(str, RhythmFeatureExtractorBase)]]=None, snap_to_grid_policy: SnapsToGridPolicy=SnapsToGridPolicy.NOT_APPLICABLE, snaps_to_grid: bool=None):
        self._subplot_layout = subplot_layout
        self._feature_extractors = feature_extractors
        self._unit = None
        self._snaps_to_grid = None
        self._snap_to_grid_policy = snap_to_grid_policy
        if snaps_to_grid is None:
            if snap_to_grid_policy in [SnapsToGridPolicy.NEVER, SnapsToGridPolicy.ADJUSTABLE]:
                snaps_to_grid = False
            elif snap_to_grid_policy == SnapsToGridPolicy.ALWAYS:
                snaps_to_grid = True
        self.snaps_to_grid = snaps_to_grid
        self.set_unit(unit)

    def set_unit(self, unit):
        if unit != 'ticks':
            Unit.check_unit(unit)
        for feature_extractor in self._feature_extractors.values():
            feature_extractor.set_unit(unit)

        self._unit = unit

    def get_unit(self):
        return self._unit

    @property
    def unit(self):
        return self.get_unit()

    @unit.setter
    def unit(self, unit):
        self.set_unit(unit)

    @property
    def snap_to_grid_policy(self):
        return self._snap_to_grid_policy

    @property
    def snaps_to_grid(self) -> bool:
        return self._snaps_to_grid

    @snaps_to_grid.setter
    def snaps_to_grid(self, snaps_to_grid):
        policy = self._snap_to_grid_policy
        if policy == SnapsToGridPolicy.NOT_APPLICABLE:
            if snaps_to_grid is not None:
                raise RuntimeError('Snaps to grid is not applicable for %s' % self.__class__.__name__)
            return
        if policy != SnapsToGridPolicy.ADJUSTABLE:
            if policy == SnapsToGridPolicy.ALWAYS:
                assert snaps_to_grid
            elif policy == SnapsToGridPolicy.NEVER:
                assert not snaps_to_grid
        snaps_to_grid = bool(snaps_to_grid)
        self._snaps_to_grid = snaps_to_grid
        for quantizable_extractor in (ext for ext in self._feature_extractors.values() if isinstance(ext, Quantizable)):
            quantizable_extractor.set_quantize_enabled(snaps_to_grid)

    def draw(self, rhythm_loop: RhythmLoop, figure: tp.Optional[plt.Figure]=None, figure_kwargs: tp.Optional[tp.Dict[(str, tp.Any)]]=None, legend_kwargs: tp.Dict[(str, tp.Any)]=None, subplot_kwargs: tp.Optional[tp.Dict[(str, tp.Any)]]=None) -> plt.Figure:
        """
        Plots the the given drum loop on a matplotlib figure and returns the figure object.

        :param rhythm_loop: the rhythm loop to plot
        :param figure: figure to draw the loop
        :param figure_kwargs: keyword arguments for the creation of the figure. This argument is ignored if a custom
                              figure has been provided
        :param subplot_kwargs: keyword arguments for the call to Figure.add_subplot
        :param legend_kwargs: keyword arguments for the call to Figure.legend
        :return: matplotlib figure object
        """
        concrete_unit = rhythm_loop.get_resolution() if self.unit == 'ticks' else self.unit
        n_tracks = rhythm_loop.get_track_count()
        plot_type_name = self.get_plot_type_name()
        figure = figure or (plt.figure)(('%s - %s' % (plot_type_name, rhythm_loop.name)), **figure_kwargs or {})
        subplots = iter(self._subplot_layout.inflate(figure, n_tracks, subplot_kwargs or dict()))
        color_pool = cycle(self.COLORS)
        prev_subplot, subplot_setup_ret = (None, None)
        common_kwargs = {'concrete_unit':concrete_unit, 
         'n_pulses':int(math.ceil(rhythm_loop.get_duration(concrete_unit))), 
         'n_tracks':rhythm_loop.get_track_count()}
        track_names = []
        subplots_handles = []
        for ix, track in enumerate(rhythm_loop.get_track_iterator()):
            subplot = next(subplots)
            if subplot != prev_subplot:
                subplot_setup_ret = (self.__setup_subplot__)(rhythm_loop, subplot, **common_kwargs)
            handle = (self.__draw_track__)(
 track, subplot, track_ix=ix, color=next(color_pool), setup_ret=subplot_setup_ret, **common_kwargs)[0]
            track_names.append(track.name)
            subplots_handles.append(handle)
            prev_subplot = subplot

        (figure.legend)(subplots_handles, track_names, loc='center right', **legend_kwargs or {})
        return figure

    def get_feature_extractor(self, feature_extractor_name):
        return self._feature_extractors[feature_extractor_name]

    @classmethod
    @abstractmethod
    def get_plot_type_name(cls):
        raise NotImplementedError

    @abstractmethod
    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        raise NotImplementedError

    @abstractmethod
    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        raise NotImplementedError


class SchillingerRhythmNotation(RhythmLoopPlotter):
    PLOT_TYPE_NAME = 'Schillinger rhythm notation'

    def __init__(self, unit='eighths'):
        super().__init__(unit=unit,
          subplot_layout=(CombinedSubplotLayout()),
          feature_extractors={'schillinger': BinarySchillingerChain()},
          snap_to_grid_policy=(SnapsToGridPolicy.ALWAYS))

    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        axes.yaxis.set_ticklabels([])
        axes.yaxis.set_visible(False)
        plot_rhythm_grid(axes, rhythm_loop, kw['concrete_unit'])

    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        lo_y = kw['track_ix'] + kw['track_ix'] * 0.25
        hi_y = lo_y + 1.0
        schillinger_extractor = self.get_feature_extractor('schillinger')
        schillinger_extractor.values = (lo_y, hi_y)
        schillinger_chain = schillinger_extractor.process(rhythm_track)
        return axes.plot(schillinger_chain, drawstyle='steps-pre', color=(kw['color']), linewidth=2.5)

    @classmethod
    def get_plot_type_name(cls):
        return cls.PLOT_TYPE_NAME


class ChronotonicNotation(RhythmLoopPlotter):
    PLOT_TYPE_NAME = 'Chronotonic notation'

    def __init__(self, unit='eighths'):
        super().__init__(unit=unit,
          subplot_layout=(CombinedSubplotLayout()),
          feature_extractors={'chronotonic': ChronotonicChain()},
          snap_to_grid_policy=(SnapsToGridPolicy.ALWAYS))

    @classmethod
    def get_plot_type_name(cls):
        return cls.PLOT_TYPE_NAME

    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        plot_rhythm_grid(axes, rhythm_loop, kw['concrete_unit'])

    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        chronotonic_chain = self.get_feature_extractor('chronotonic').process(rhythm_track)
        return axes.plot(chronotonic_chain, '--.', color=(kw['color']))


class PolygonNotation(RhythmLoopPlotter):
    PLOT_TYPE_NAME = 'Polygon notation'

    def __init__(self, unit='eighths'):
        super().__init__(unit=unit,
          subplot_layout=(CombinedSubplotLayout()),
          feature_extractors={'onset_positions': OnsetPositionVector()},
          snap_to_grid_policy=(SnapsToGridPolicy.ADJUSTABLE))

    @classmethod
    def get_plot_type_name(cls):
        return cls.PLOT_TYPE_NAME

    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        axes.axis('equal')
        axes.axis([0, 1, 0, 1])
        main_radius = 0.3
        main_center = (0.5, 0.5)

        def draw_wedge(pulse_start, pulse_end, center=main_center, radius=main_radius, **kw_):
            theta_1, theta_2 = ((90 - pulse / n_pulses * 360) % 360 for pulse in (pulse_end, pulse_start))
            axes.add_artist(Wedge(center, radius, theta_1, theta_2, **kw_))

        unit = kw['concrete_unit']
        n_pulses = kw['n_pulses']
        n_pulses_per_measure = int(rhythm_loop.get_measure_duration(unit))
        try:
            n_measures = int(n_pulses / n_pulses_per_measure)
        except ZeroDivisionError:
            n_measures = 0

        for i_measure in range(0, n_measures, 2):
            from_pulse = i_measure * n_pulses_per_measure
            to_pulse = (i_measure + 1) * n_pulses_per_measure
            draw_wedge(from_pulse, to_pulse, radius=1.0, fc=(to_rgba('gray', 0.25)))

        circle = plt.Circle(main_center, main_radius, fc='white')
        axes.add_artist(circle)
        for i_pulse in range(0, n_pulses, 2):
            draw_wedge(i_pulse, (i_pulse + 1), fc=(to_rgba('gray', 0.25)))

        return circle

    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        n_pulses = kw['n_pulses']
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.xaxis.set_ticklabels([])
        axes.yaxis.set_ticklabels([])
        main_center = kw['setup_ret'].center
        main_radius = kw['setup_ret'].radius
        onset_times = self.get_feature_extractor('onset_positions').process(rhythm_track)
        coordinates_x = []
        coordinates_y = []
        for t in onset_times:
            relative_t = float(t) / n_pulses
            x, y = get_coordinates_on_circle(main_center, main_radius, relative_t)
            coordinates_x.append(x)
            coordinates_y.append(y)

        coordinates_x.append(coordinates_x[0])
        coordinates_y.append(coordinates_y[0])
        return axes.plot(coordinates_x, coordinates_y, '-o', color=(kw['color']))


class SpectralNotation(RhythmLoopPlotter):
    PLOT_TYPE_NAME = 'Spectral notation'

    def __init__(self, unit='eighths'):
        super().__init__(unit=unit,
          subplot_layout=(StackedSubplotLayout(Orientation.VERTICAL)),
          feature_extractors={'ioi_vector': IOIVector()},
          snap_to_grid_policy=(SnapsToGridPolicy.ADJUSTABLE))

    @classmethod
    def get_plot_type_name(cls):
        return cls.PLOT_TYPE_NAME

    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        axes.xaxis.set_visible(False)
        axes.xaxis.set_ticklabels([])

    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        ioi_vector = self.get_feature_extractor('ioi_vector').process(rhythm_track)
        return axes.bar((list(range(len(ioi_vector)))), ioi_vector, width=0.95, color=(kw['color']))


class TEDASNotation(RhythmLoopPlotter):
    PLOT_TYPE_NAME = 'TEDAS Notation'

    def __init__(self, unit='eighths'):
        super().__init__(unit=unit,
          subplot_layout=(StackedSubplotLayout(Orientation.VERTICAL)),
          feature_extractors={'onset_positions':OnsetPositionVector(quantize_enabled=True), 
         'ioi_vector':IOIVector(quantize_enabled=True)},
          snap_to_grid_policy=(SnapsToGridPolicy.ADJUSTABLE))

    @classmethod
    def get_plot_type_name(cls):
        return cls.PLOT_TYPE_NAME

    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        plot_rhythm_grid(axes, rhythm_loop, kw['concrete_unit'])

    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        ioi_vector = self.get_feature_extractor('ioi_vector').process(rhythm_track)
        onset_positions = self.get_feature_extractor('onset_positions').process(rhythm_track)
        styles = {'edgecolor':kw['color'], 
         'facecolor':colors.to_rgba(kw['color'], 0.18), 
         'linewidth':2.0}
        return (axes.bar)(onset_positions, ioi_vector, width=ioi_vector, align='edge', **styles)


class IOIHistogramPlot(RhythmLoopPlotter):
    PLOT_TYPE_NAME = 'Inter-onset interval histogram'

    def __init__(self, unit='eighths'):
        super().__init__(unit=unit,
          subplot_layout=(CombinedSubplotLayout()),
          feature_extractors={'ioi_histogram': IOIHistogram()},
          snap_to_grid_policy=(SnapsToGridPolicy.NOT_APPLICABLE))

    @classmethod
    def get_plot_type_name(cls):
        return cls.PLOT_TYPE_NAME

    def __setup_subplot__(self, rhythm_loop: RhythmLoop, axes: plt.Axes, **kw):
        pass

    def __draw_track__(self, rhythm_track: Track, axes: plt.Axes, **kw):
        occurrences, interval_durations = self.get_feature_extractor('ioi_histogram').process(rhythm_track)
        return axes.bar(interval_durations, occurrences, color=(kw['color']))


def get_rhythm_loop_plotter_classes():
    """Returns RhythmLoopPlotter subclasses

    :return: RhythmLoopPlotter subclasses as a list
    """
    return RhythmLoopPlotter.__subclasses__()


__all__ = [
 'RhythmLoopPlotter',
 'SchillingerRhythmNotation', 'ChronotonicNotation', 'PolygonNotation',
 'SpectralNotation', 'TEDASNotation', 'IOIHistogram', 'get_rhythm_loop_plotter_classes',
 'SubplotLayout', 'CombinedSubplotLayout', 'StackedSubplotLayout', 'Orientation',
 'SnapsToGridPolicy', 'plot_rhythm_grid']