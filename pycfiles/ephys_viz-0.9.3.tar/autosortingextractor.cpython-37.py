# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/pycommon/autoextractors/autosortingextractor.py
# Compiled at: 2019-11-19 08:44:15
# Size of source mod 2**32: 4298 bytes
import kachery as ka, spikeextractors as se, h5py, numpy as np
from .mdaextractors import MdaSortingExtractor
import pycommon.load_nwb_item as load_nwb_item

class AutoSortingExtractor(se.SortingExtractor):

    def __init__(self, arg):
        super().__init__()
        self._hash = None
        if isinstance(arg, se.SortingExtractor):
            self._sorting = arg
            self.copy_unit_properties(sorting=(self._sorting))
        else:
            self._sorting = None
            if 'kachery_config' in arg:
                (ka.set_config)(**arg['kachery_config'])
            elif 'path' in arg:
                path = arg['path']
                if ka.get_file_info(path):
                    file_path = ka.load_file(path)
                    if not file_path:
                        raise Exception('Unable to realize file: {}'.format(path))
                    self._init_from_file(file_path, original_path=path, kwargs=arg)
                else:
                    raise Exception('Not a file: {}'.format(path))
            else:
                raise Exception('Unable to initialize sorting extractor')

    def _init_from_file(self, path: str, *, original_path: str, kwargs: dict):
        if 'nwb_path' in kwargs:
            self._sorting = NwbSortingExtractor(path=path, nwb_path=(kwargs['nwb_path']))
        else:
            if original_path.endswith('.mda'):
                if 'paramsPath' in kwargs:
                    params = ka.load_object(kwargs['paramsPath'])
                    samplerate = params['samplerate']
                else:
                    if 'samplerate' in kwargs:
                        samplerate = kwargs['samplerate']
                    else:
                        raise Exception('Missing argument: samplerate or paramsPath')
                self._sorting = MdaSortingExtractor(firings_file=path, samplerate=samplerate)
            else:
                raise Exception('Unsupported format for {}'.format(original_path))

    def hash(self):
        if not self._hash:
            if hasattr(self._sorting, 'hash'):
                if type(self._sorting.hash) == str:
                    self._hash = self._sorting.hash
                else:
                    self._hash = self._sorting.hash()
            else:
                self._hash = None
        return self._hash

    def get_unit_ids(self):
        return self._sorting.get_unit_ids()

    def get_unit_spike_train(self, **kwargs):
        return (self._sorting.get_unit_spike_train)(**kwargs)

    def get_sampling_frequency(self):
        return self._sorting.get_sampling_frequency()


class NwbSortingExtractor(se.SortingExtractor):

    def __init__(self, *, path, nwb_path):
        super().__init__()
        self._path = path
        with h5py.File(self._path, 'r') as (f):
            X = load_nwb_item(file=f, nwb_path=nwb_path)
            self._spike_times = X['spike_times'][:] * self.get_sampling_frequency()
            self._spike_times_index = X['spike_times_index'][:]
            self._unit_ids = X['id'][:]
            self._index_by_id = dict()
            for index, id0 in enumerate(self._unit_ids):
                self._index_by_id[id0] = index

    def get_unit_ids(self):
        return [int(val) for val in self._unit_ids]

    def get_unit_spike_train(self, unit_id, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        else:
            if end_frame is None:
                end_frame = np.Inf
            index = self._index_by_id[unit_id]
            ii2 = self._spike_times_index[index]
            if index - 1 >= 0:
                ii1 = self._spike_times_index[(index - 1)]
            else:
                ii1 = 0
        return self._spike_times[ii1:ii2]

    def get_sampling_frequency(self):
        return 30000