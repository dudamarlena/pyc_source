# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/honza/code/my/physt/tests/../physt/histogram1d.py
# Compiled at: 2019-10-24 06:06:27
# Size of source mod 2**32: 20679 bytes
"""One-dimensional histograms."""
from typing import Optional, Tuple
import numpy as np
from . import bin_utils
from .histogram_base import HistogramBase
from .binnings import BinningBase

class Histogram1D(HistogramBase):
    __doc__ = 'One-dimensional histogram data.\n\n    The bins can be of different widths.\n\n    The bins need not be consecutive. However, some functionality may not be available\n    for non-consecutive bins (like keeping information about underflow and overflow).\n\n    Attributes\n    ----------\n    _stats : dict\n\n\n    These are the basic attributes that can be used in the constructor (see there)\n    Other attributes are dynamic.\n    '

    def __init__(self, binning, frequencies=None, errors2=None, *, stats=None, **kwargs):
        """Constructor

        Parameters
        ----------
        binning: physt.binnings.BinningBase or array_like
            The binning
        frequencies: Optional[array_like]
            The bin contents.
        keep_missed: Optional[bool]
            Whether to keep track of underflow/overflow when filling with new values.
        underflow: Optional[float]
            Weight of observations that were smaller than the minimum bin.
        overflow: Optional[float]
            Weight of observations that were larger than the maximum bin.
        name: Optional[str]
            Name of the histogram (will be displayed as plot title)
        axis_name: Optional[str]
            Name of the characteristics that is histogrammed (will be displayed on x axis)
        errors2: Optional[array_like]
            Quadratic errors of individual bins. If not set, defaults to frequencies.
        stats: dict
            Dictionary of various statistics ("sum", "sum2")
        """
        missed = [
         kwargs.pop('underflow', 0),
         kwargs.pop('overflow', 0),
         kwargs.pop('inner_missed', 0)]
        if 'axis_name' in kwargs:
            kwargs['axis_names'] = [
             kwargs.pop('axis_name')]
        else:
            (HistogramBase.__init__)(self, [binning], frequencies, errors2, **kwargs)
            if frequencies is None:
                self._stats = Histogram1D.EMPTY_STATS.copy()
            else:
                self._stats = stats
            if self.keep_missed:
                self._missed = np.array(missed, dtype=(self.dtype))
            else:
                self._missed = np.zeros(3, dtype=(self.dtype))

    EMPTY_STATS = {'sum':0.0, 
     'sum2':0.0}

    @property
    def axis_name(self) -> str:
        return self.axis_names[0]

    @axis_name.setter
    def axis_name(self, value: str):
        self.axis_names = (value,)

    def select(self, axis, index, force_copy: bool=False):
        """Alias for [] to be compatible with HistogramND."""
        if axis == 0:
            if index == slice(None):
                if not force_copy:
                    return self
            return self[index]
        raise ValueError('In Histogram1D.select(), axis must be 0.')

    def __getitem__(self, i):
        """Select sub-histogram or get one bin.

        Parameters
        ----------
        i : int or slice or bool masked array or array with indices
            In most cases, this has same semantics as for numpy.ndarray.__getitem__

        Returns
        -------
        Histogram1D or tuple
            Depending on the parameters, a sub-histogram or content of one bin are returned.
        """
        underflow = np.nan
        overflow = np.nan
        keep_missed = False
        if isinstance(i, int):
            return (
             self.bins[i], self.frequencies[i])
            if isinstance(i, np.ndarray):
                if i.dtype == bool and i.shape != (self.bin_count,):
                    raise IndexError('Cannot index with masked array of a wrong dimension')
        elif isinstance(i, slice):
            keep_missed = self.keep_missed
            if i.step:
                raise IndexError('Cannot change the order of bins')
            if i.step == 1 or i.step is None:
                underflow = self.underflow
                overflow = self.overflow
                if i.start:
                    underflow += self.frequencies[0:i.start].sum()
                if i.stop:
                    overflow += self.frequencies[i.stop:].sum()
        return self.__class__((self._binning.as_static(copy=False)[i]), (self.frequencies[i]), (self.errors2[i]),
          overflow=overflow, keep_missed=keep_missed, underflow=underflow,
          dtype=(self.dtype),
          name=(self.name),
          axis_name=(self.axis_name))

    @property
    def _binning(self) -> BinningBase:
        """Adapter property for HistogramBase interface"""
        return self._binnings[0]

    @_binning.setter
    def _binning(self, value: BinningBase):
        self._binnings = [value]

    @property
    def binning(self) -> BinningBase:
        """The binning.

        Note: Please, do not try to update the object itself.
        """
        return self._binning

    @property
    def bins(self) -> np.ndarray:
        """Array of all bin edges.

        Returns
        -------
        Wide-format [[leftedge1, rightedge1], ... [leftedgeN, rightedgeN]]
        """
        return self._binning.bins

    @property
    def numpy_bins(self) -> np.ndarray:
        """Bins in the format of numpy.
        """
        return self._binning.numpy_bins

    @property
    def edges(self) -> np.ndarray:
        return self.numpy_bins

    @property
    def numpy_like(self) -> Tuple[(np.ndarray, np.ndarray)]:
        """Same result as would the numpy.histogram function return."""
        return (
         self.frequencies, self.numpy_bins)

    @property
    def cumulative_frequencies(self) -> np.ndarray:
        """Cumulative frequencies.

        Note: underflow values are not considered
        """
        return self._frequencies.cumsum()

    @property
    def underflow(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[0]

    @underflow.setter
    def underflow(self, value):
        self._missed[0] = value

    @property
    def overflow(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[1]

    @overflow.setter
    def overflow(self, value):
        self._missed[1] = value

    @property
    def inner_missed(self):
        if not self.keep_missed:
            return np.nan
        return self._missed[2]

    @inner_missed.setter
    def inner_missed(self, value):
        self._missed[2] = value

    def mean(self) -> Optional[float]:
        """Statistical mean of all values entered into histogram.

        This number is precise, because we keep the necessary data
        separate from bin contents.
        """
        if self._stats:
            if self.total > 0:
                return self._stats['sum'] / self.total
            return np.nan
        else:
            return

    def std(self) -> Optional[float]:
        """Standard deviation of all values entered into histogram.

        This number is precise, because we keep the necessary data
        separate from bin contents.

        Returns
        -------
        float
        """
        if self._stats:
            return np.sqrt(self.variance())
        return

    def variance(self) -> Optional[float]:
        """Statistical variance of all values entered into histogram.

        This number is precise, because we keep the necessary data
        separate from bin contents.

        Returns
        -------
        float
        """
        if self._stats:
            if self.total > 0:
                return (self._stats['sum2'] - self._stats['sum'] ** 2 / self.total) / self.total
            return np.nan
        else:
            return

    @property
    def bin_left_edges(self):
        """Left edges of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return self.bins[(Ellipsis, 0)]

    @property
    def bin_right_edges(self):
        """Right edges of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return self.bins[(Ellipsis, 1)]

    @property
    def min_edge(self):
        """Left edge of the first bin.

        Returns
        -------
        float
        """
        return self.bin_left_edges[0]

    @property
    def max_edge(self):
        """Right edge of the last bin.

        Returns
        -------
        float
        """
        return self.bin_right_edges[(-1)]

    @property
    def bin_centers(self):
        """Centers of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return (self.bin_left_edges + self.bin_right_edges) / 2

    @property
    def bin_widths(self):
        """Widths of all bins.

        Returns
        -------
        numpy.ndarray
        """
        return self.bin_right_edges - self.bin_left_edges

    @property
    def total_width(self):
        """Total width of all bins.

        In inconsecutive histograms, the missing intervals are not counted in.

        Returns
        -------
        float
        """
        return self.bin_widths.sum()

    @property
    def bin_sizes(self):
        return self.bin_widths

    def find_bin(self, value):
        """Index of bin corresponding to a value.

        Parameters
        ----------
        value: float
            Value to be searched for.

        Returns
        -------
        int
            index of bin to which value belongs
            (-1=underflow, N=overflow, None=not found - inconsecutive)
        """
        ixbin = np.searchsorted((self.bin_left_edges), value, side='right')
        if ixbin == 0:
            return -1
            if ixbin == self.bin_count:
                if value <= self.bin_right_edges[(-1)]:
                    return ixbin - 1
                return self.bin_count
        else:
            if value < self.bin_right_edges[(ixbin - 1)]:
                return ixbin - 1
            if ixbin == self.bin_count:
                return self.bin_count
            return

    def fill(self, value: float, weight: float=1) -> int:
        """Update histogram with a new value.

        Parameters
        ----------
        value: float
            Value to be added.
        weight: float, optional
            Weight assigned to the value.

        Returns
        -------
        int
            index of bin which was incremented (-1=underflow, N=overflow, None=not found)

        Note: If a gap in unconsecutive bins is matched, underflow & overflow are not valid anymore.
        Note: Name was selected because of the eponymous method in ROOT
        """
        self._coerce_dtype(type(weight))
        if self._binning.is_adaptive():
            map = self._binning.force_bin_existence(value)
            self._reshape_data(self._binning.bin_count, map)
        else:
            ixbin = self.find_bin(value)
            if ixbin is None:
                self.overflow = np.nan
                self.underflow = np.nan
            else:
                if ixbin == -1 and self.keep_missed:
                    self.underflow += weight
                else:
                    if ixbin == self.bin_count and self.keep_missed:
                        self.overflow += weight
                    else:
                        self._frequencies[ixbin] += weight
                        self._errors2[ixbin] += weight ** 2
                        if self._stats:
                            self._stats['sum'] += weight * value
                            self._stats['sum2'] += weight * value ** 2
        return ixbin

    def fill_n(self, values, weights=None, dropna: bool=True):
        """Update histograms with a set of values.

        Parameters
        ----------
        values: array_like
        weights: Optional[array_like]
        drop_na: Optional[bool]
            If true (default), all nan's are skipped.
        """
        values = np.asarray(values)
        if dropna:
            values = values[(~np.isnan(values))]
        if self._binning.is_adaptive():
            map = self._binning.force_bin_existence(values)
            self._reshape_data(self._binning.bin_count, map)
        if weights is not None:
            weights = np.asarray(weights)
            self._coerce_dtype(weights.dtype)
        frequencies, errors2, underflow, overflow, stats = calculate_frequencies(values, (self._binning), dtype=(self.dtype), weights=weights,
          validate_bins=False)
        self._frequencies += frequencies
        self._errors2 += errors2
        if self.keep_missed:
            self.underflow += underflow
            self.overflow += overflow
        if self._stats:
            for key in self._stats:
                self._stats[key] += stats.get(key, 0.0)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            if not np.allclose(other.bins, self.bins):
                return False
            else:
                if not np.allclose(other.frequencies, self.frequencies):
                    return False
                else:
                    if not np.allclose(other.errors2, self.errors2):
                        return False
                    else:
                        if not other.overflow == self.overflow:
                            return False
                        return other.underflow == self.underflow or False
                    return other.inner_missed == self.inner_missed or False
                return other.name == self.name or False
            return other.axis_name == self.axis_name or False
        return True

    def to_dataframe(self) -> 'pandas.DataFrame':
        """Convert to pandas DataFrame.

        This is not a lossless conversion - (under/over)flow info is lost.
        """
        import pandas as pd
        df = pd.DataFrame({'left':self.bin_left_edges, 
         'right':self.bin_right_edges, 
         'frequency':self.frequencies, 
         'error':self.errors},
          columns=[
         'left', 'right', 'frequency', 'error'])
        return df

    @classmethod
    def _kwargs_from_dict(cls, a_dict: dict) -> dict:
        kwargs = HistogramBase._kwargs_from_dict.__func__(cls, a_dict)
        kwargs['binning'] = kwargs.pop('binnings')[0]
        return kwargs

    def to_xarray(self) -> 'xarray.Dataset':
        """Convert to xarray.Dataset"""
        import xarray as xr
        data_vars = {'frequencies':xr.DataArray(self.frequencies, dims='bin'), 
         'errors2':xr.DataArray(self.errors2, dims='bin'), 
         'bins':xr.DataArray(self.bins, dims=('bin', 'x01'))}
        coords = {}
        attrs = {'underflow':self.underflow, 
         'overflow':self.overflow, 
         'inner_missed':self.inner_missed, 
         'keep_missed':self.keep_missed}
        attrs.update(self._meta_data)
        return xr.Dataset(data_vars, coords, attrs)

    @classmethod
    def from_xarray(cls, arr: 'xarray.Dataset') -> 'Histogram1D':
        """Convert form xarray.Dataset

        Parameters
        ----------
        arr: The data in xarray representation
        """
        kwargs = {'frequencies':arr['frequencies'], 
         'binning':arr['bins'], 
         'errors2':arr['errors2'], 
         'overflow':arr.attrs['overflow'], 
         'underflow':arr.attrs['underflow'], 
         'keep_missed':arr.attrs['keep_missed']}
        return cls(**kwargs)


def calculate_frequencies(data, binning, weights=None, *, validate_bins=True, already_sorted: bool=False, dtype=None):
    """Get frequencies and bin errors from the data.

    Parameters
    ----------
    data : array_like
        Data items to work on.
    binning : physt.binnings.BinningBase
        A set of bins.
    weights : array_like, optional
        Weights of the items.
    validate_bins : bool, optional
        If True (default), bins are validated to be in ascending order.
    already_sorted : bool, optional
        If True, the data being entered are already sorted, no need to sort them once more.
    dtype: Optional[type]
        Underlying type for the histogram.
        (If weights are specified, default is float. Otherwise long.)

    Returns
    -------
    frequencies : numpy.ndarray
        Bin contents
    errors2 : numpy.ndarray
        Error squares of the bins
    underflow : float
        Weight of items smaller than the first bin
    overflow : float
        Weight of items larger than the last bin
    stats: dict
        { sum: ..., sum2: ...}

    Note
    ----
    Checks that the bins are in a correct order (not necessarily consecutive).
    Does not check for numerical overflows in bins.
    """
    sum = 0.0
    sum2 = 0.0
    bins = binning.bins
    if validate_bins:
        if bins.shape[0] == 0:
            raise RuntimeError('Cannot have histogram with 0 bins.')
        if not bin_utils.is_rising(bins):
            raise RuntimeError('Bins must be rising.')
    data = np.asarray(data)
    if data.ndim > 1:
        data = data.flatten()
    if weights is not None:
        weights = np.asarray(weights)
        if weights.ndim > 1:
            weights = weights.flatten()
        if weights.shape != data.shape:
            raise RuntimeError('Weights must have the same shape as data.')
        if dtype is None:
            dtype = weights.dtype
    if dtype is None:
        dtype = int
    dtype = np.dtype(dtype)
    if dtype.kind in 'iu':
        if weights is not None:
            if weights.dtype.kind == 'f':
                raise RuntimeError('Integer histogram requested but float weights entered.')
    if not already_sorted:
        args = np.argsort(data)
        data = data[args]
        if weights is not None:
            weights = weights[args]
        del args
    frequencies = np.zeros((bins.shape[0]), dtype=dtype)
    errors2 = np.zeros((bins.shape[0]), dtype=dtype)
    for xbin, bin in enumerate(bins):
        start = np.searchsorted(data, (bin[0]), side='left')
        stop = np.searchsorted(data, (bin[1]), side='left')
        if xbin == 0:
            if weights is not None:
                underflow = weights[0:start].sum()
            else:
                underflow = start
        if xbin == len(bins) - 1:
            stop = np.searchsorted(data, (bin[1]), side='right')
            if weights is not None:
                overflow = weights[stop:].sum()
            else:
                overflow = data.shape[0] - stop
        if weights is not None:
            frequencies[xbin] = weights[start:stop].sum()
            errors2[xbin] = (weights[start:stop] ** 2).sum()
            sum += (data[start:stop] * weights[start:stop]).sum()
            sum2 += (data[start:stop] ** 2 * weights[start:stop]).sum()
        else:
            frequencies[xbin] = stop - start
            errors2[xbin] = stop - start
            sum += data[start:stop].sum()
            sum2 += (data[start:stop] ** 2).sum()
    else:
        if not bin_utils.is_consecutive(bins):
            underflow = np.nan
            overflow = np.nan
        stats = {'sum':sum,  'sum2':sum2}
        return (
         frequencies, errors2, underflow, overflow, stats)