# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/honza/code/my/physt/physt/histogram_collection.py
# Compiled at: 2019-10-30 16:46:57
# Size of source mod 2**32: 6312 bytes
from typing import Optional, Container, Tuple, Dict, Any
import sys, numpy as np
from .histogram1d import Histogram1D
from .binnings import BinningBase
from . import h1

class HistogramCollection(Container[Histogram1D]):
    __doc__ = 'Experimental collection of histograms.\n    \n    It contains (potentially name-addressable) histograms\n    with a shared binning.\n    '

    def __init__(self, *histograms: Histogram1D, binning: Optional[BinningBase]=None, title: Optional[str]=None, name: Optional[str]=None):
        self.histograms = list(histograms)
        if histograms:
            if binning:
                raise ValueError('')
            self._binning = histograms[0].binning
            assert all((h.binning == self._binning for h in histograms)), 'All histogram should share the same binning.'
        else:
            self._binning = binning
        self.name = name
        self.title = title or self.name

    def __contains__--- This code section failed: ---

 L.  36         0  SETUP_FINALLY        16  'to 16'

 L.  37         2  LOAD_FAST                'self'
                4  LOAD_FAST                'item'
                6  BINARY_SUBSCR    
                8  STORE_FAST               '_'

 L.  38        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  39        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  40        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14

    @property
    def ndim(self) -> int:
        return 1

    def __iter__(self):
        return iter(self.histograms)

    def __len__(self):
        return len(self.histograms)

    def copy(self) -> 'HistogramCollection':
        copy_binning = self.binning.copy()
        histograms = [h.copy() for h in self.histograms]
        for h in histograms:
            h._binning = copy_binning
        else:
            return HistogramCollection(*histograms, title=self.title, 
             name=self.name)

    @property
    def binning(self) -> BinningBase:
        return self._binning

    @property
    def bins(self) -> np.ndarray:
        return self.binning.bins

    @property
    def axis_name(self) -> Optional[str]:
        return self.histograms and self.histograms[0].axis_name or None

    @property
    def axis_names(self) -> Tuple[str]:
        return (self.axis_name,)

    def add(self, histogram: Histogram1D):
        """Add a histogram to the collection."""
        if self.binning:
            if not self.binning == histogram.binning:
                raise ValueError('Cannot add histogram with different binning.')
        self.histograms.append(histogram)

    def create(self, name: str, values, *, weights=None, dropna: bool=True, **kwargs):
        init_kwargs = {'axis_name': self.axis_name}
        init_kwargs.update(kwargs)
        histogram = Histogram1D(binning=self.binning, name=name, **init_kwargs)
        histogram.fill_n(values, weights=weights, dropna=dropna)
        self.histograms.append(histogram)
        return histogram

    def __getitem__(self, item) -> Histogram1D:
        if isinstance(item, str):
            candidates = [h for h in self.histograms if h.name == item]
            if len(candidates) == 0:
                raise KeyError('Collection does not contain histogram named {0}'.format(item))
            return candidates[0]
        return self.histograms[item]

    def __eq__(self, other) -> bool:
        return type(other) == HistogramCollection and len(other) == len(self) and all((h1 == h2 for h1, h2 in zip(self.histograms, other.histograms)))

    def normalize_bins(self, inplace: bool=False) -> 'HistogramCollection':
        """Normalize each bin in the collection so that the sum is 1.0 for each bin.

        Note: If a bin is zero in all collections, the result will be inf.
        """
        col = self if inplace else self.copy()
        sums = self.sum().frequencies
        for h in col.histograms:
            h.set_dtype(float)
            h._frequencies /= sums
            h._errors2 /= sums ** 2
        else:
            return col

    def normalize_all(self, inplace: bool=False) -> 'HistogramCollection':
        """Normalize all histograms so that total content of each of them is equal to 1.0."""
        col = self if inplace else self.copy()
        for h in col.histograms:
            h.normalize(inplace=True)
        else:
            return col

    def sum(self) -> Histogram1D:
        """Return the sum of all contained histograms."""
        return sum(self.histograms)

    @property
    def plot(self) -> 'physt.plotting.PlottingProxy':
        """Proxy to plotting.

        This attribute is a special proxy to plotting. In the most
        simple cases, it can be used as a method. For more sophisticated
        use, see the documentation for physt.plotting package.
        """
        from .plotting import PlottingProxy
        return PlottingProxy(self)

    @classmethod
    def multi_h1(cls, a_dict: Dict[(str, Any)], bins=None, **kwargs) -> 'HistogramCollection':
        """Create a collection from multiple datasets."""
        from physt.binnings import calculate_bins
        mega_values = np.concatenate(list(a_dict.values()))
        binning = calculate_bins(mega_values, bins, **kwargs)
        title = kwargs.pop('title', None)
        name = kwargs.pop('name', None)
        collection = HistogramCollection(binning=binning, title=title, name=name)
        for key, value in a_dict.items():
            collection.create(key, value)
        else:
            return collection

    @classmethod
    def from_dict(cls, a_dict: dict) -> 'HistogramCollection':
        from physt.io import create_from_dict
        col = HistogramCollection()
        for item in a_dict['histograms']:
            h = create_from_dict(item, 'HistogramCollection', check_version=False)
            col.add(h)
        else:
            return col

    def to_dict(self) -> dict:
        return {'histogram_type':'histogram_collection', 
         'histograms':[h.to_dict() for h in self.histograms]}

    def to_json(self, path: Optional[str]=None, **kwargs) -> str:
        """Convert to JSON representation.

        Parameters
        ----------
        path: Where to write the JSON.

        Returns
        -------
        The JSON representation.
        """
        from .io import save_json
        return save_json(self, path, **kwargs)