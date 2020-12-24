# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/signal/timeseriesLF.py
# Compiled at: 2018-11-24 16:08:24
# Size of source mod 2**32: 12707 bytes
from ptsa.data.timeseries import TimeSeries
try:
    from mne.io import read_raw_edf
except ImportError:
    read_raw_edf = None

import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
from datetime import datetime, date
from pyedflib import EdfWriter
import xarray as xr, numpy as np
import IPython.display as display
import pyedflib
__all__ = [
 'TimeSeriesLF']

class TimeSeriesLF(TimeSeries):
    __doc__ = 'A thin wrapper around :class:`xr.DataArray` for dealing with time series\n    data and timeseries.\n    Note that xarray internals prevent us from overriding the constructor which\n    leads to some awkwardness: you must pass coords as a dict with a\n    ``samplerate`` entry.\n    Parameters\n    ----------\n    data : array-like\n        Time series data\n    coords : dict-like\n        Coordinate arrays. This must contain at least a ``samplerate``\n        coordinate.\n    dims : array-like\n        Dimension labels\n    name : str\n        Name of the time series\n    attrs : dict\n        Dictionary of arbitrary metadata\n    encoding : dict\n    fastpath : bool\n        Not used, but required when subclassing :class:`xr.DataArray`.\n    Raises\n    ------\n    AssertionError\n        When ``samplerate`` is not present in ``coords``.\n    See also\n    --------\n    xr.DataArray : Base class\n    '

    def __init__(self, data, coords, dims=None, name=None, attrs=None, encoding=None, fastpath=False):
        assert 'samplerate' in coords
        super(TimeSeriesLF, self).__init__(data=data, coords=coords, dims=dims, name=name,
          attrs=attrs,
          encoding=encoding,
          fastpath=fastpath)

    @classmethod
    def from_edf(cls, filename, correct_channels=None, *args, **kwargs):
        """Takes a file located at filename and returns it as a TimeSeriesX object

        FIXME: automate the generation of 'events' based upon raw signal for _sleep data

        ------
        INPUTS
        filename: str, path to the edf file, e.g. '/Volumes/rhino/home2/loganf/data.edf'

        ------
        OUTPUTS
        ts: TimeSeriesX

        Parameters
        ----------
        filename : str

        """
        if read_raw_edf is None:
            raise RuntimeError('You must install mne to load from EDF')
        print('Extracting edf signal from {}'.format(filename))
        raw_data = read_raw_edf(filename, *args, preload=False, verbose='ERROR', stim_channel=None, **kwargs)
        if correct_channels is not None:
            matched = cls.get_eeg_ch_matches(raw_data.ch_names, correct_channels)
            all_chs = np.arange(len(raw_data.ch_names))
            bad_indx = [x for x in all_chs if x not in matched]
            exclude = list(np.array(raw_data.ch_names)[bad_indx])
            raw_data = read_raw_edf(filename, *args, stim_channel=None, exclude=exclude, preload=True, verbose='ERROR', **kwargs)
        else:
            if correct_channels is None:
                if raw_data.ch_names[(-1)] in ('EDF Annotations', 'STI 014'):
                    raw_data = read_raw_edf(filename, *args, stim_channel=None, exclude=raw_data.ch_names[(-1)], preload=True, verbose='ERROR', **kwargs)
                else:
                    raw_data.load_data()
        data, chs, sfreq = raw_data._data, raw_data.ch_names, np.round(raw_data.info['sfreq'])
        time = np.arange(0, data.shape[(-1)]) / sfreq
        coords = {'channels':chs, 
         'time':time,  'samplerate':sfreq}
        ts = cls.create(data, sfreq, coords=coords, dims=[
         'channels', 'time'])
        print('Ready.')
        return ts

    @classmethod
    def concat(cls, ts_list, dim='events', *args, **kwargs):
        """Concatenates a list of TimeSeriesX objects along a dimension

        FIX ME: Change to check if any dim is np.recarray and reset any that are.
        -----
        INPUTS
        ts_list: list, a list of time_series seperated, e.g. list of sessions
        dim: str, dimension to concatenate over, you can also choose a new name (e.g. 'subjects'
             across all a list of all subjects). By default tries to do events
        -----
        OUTPUTS
        ts: TimeSeriesX Object, a functional timeseries object with indexable events
        """
        if all(['events' in y for y in [x.dims for x in ts_list]]):
            evs = np.concatenate([x.events.data for x in ts_list]).view(np.recarray)
            ts = (xr.concat)(args, objs=ts_list, dim=dim, **kwargs)
            ts['events'] = evs
            return ts
        try:
            ts = (xr.concat)(args, objs=ts_list, dim=dim, **kwargs)
            return ts
        except:
            print(ts_list[0].dims)
            print('There needs to be an "events" dim for each of the TimeSeriesX in the passed list')
            assert all(['events' in y for y in [x.dims for x in ts_list]])

    def to_edf(self, save_path, annotations=None, header=None):
        valid = np.array(['channel', 'channels', 'bipolar_pair', 'bipolar_pairs'])
        label = valid[np.where(np.in1d(valid, np.intersect1d(np.array(self.dims), valid)))][0]
        try:
            assert label == self.dims[0]
        except AssertionError:
            raise AssertionError('Please ensure that the first dimension of the timeseries is {}'.format(label))

        n_valid_signals = self[label].shape[0]
        writer = EdfWriter(save_path, n_channels=n_valid_signals, file_type=(pyedflib.FILETYPE_EDFPLUS))
        channel_info, data_list = [], []
        physical_maximums = self.max('time')
        physical_minimums = self.min('time')
        for i in np.arange(n_valid_signals):
            ch_dict = {'label':str(self[label][i].data),  'dimension':'uV', 
             'sample_rate':float(self.samplerate.data), 
             'physical_max':float(physical_maximums[i]), 
             'physical_min':float(physical_minimums[i]), 
             'digital_max':32767.0, 
             'digital_min':-32768.0, 
             'transducer':'', 
             'prefilter':''}
            channel_info.append(ch_dict)
            data_list.append(self[i].data)

        if annotations is not None:
            for annotation in annotations:
                writer.writeAnnotation(annotation[0], -1, annotation[2])

        if header is None:
            header = {'technician':'', 
             'recording_additional':'', 
             'patientname':'No Name', 
             'patient_additional':'', 
             'patientcode':'0', 
             'equipment':'NKC-EEG-1200A V01.00', 
             'admincode':'', 
             'gender':'', 
             'startdate':datetime(2017, 8, 17, 1, 4, 43), 
             'birthdate':date(1951, 8, 2)}
        header = {'technician':'tec1',  'recording_additional':'recAdd1',  'patientname':'pat1',  'patient_additional':'patAdd1', 
         'patientcode':'code1',  'equipment':'eq1',  'admincode':'admin1', 
         'gender':1,  'startdate':datetime(2017, 1, 1, 1, 1, 1),  'birthdate':date(1951, 8, 2)}
        writer.setHeader(header)
        writer.setSignalHeaders(channel_info)
        writer.writePhysicalSamples(data_list)
        writer.close()

    @staticmethod
    def get_eeg_ch_matches(signal_labels, contacts_label):
        """ This is used in cases where we want to load data raw off the clinical record and replace bad names with good names
        f = EdfReader(file_name=file_path)
        signal_labels = f.getSignalLabels()
        reader = CMLReader(subject='R1207J', experiment="FR1", session=1,
                           localization=0, montage=0)
        df = reader.load('contacts')
        contacts_label = np.array(df['label'])
        """
        signal_labels = np.array([label.upper() for label in signal_labels])
        match_index = []
        for channel in contacts_label:
            match = np.flatnonzero(np.core.defchararray.find(signal_labels, channel) != -1)
            if match.size > 0:
                match_index.append(match)

        match_index = np.unique(np.concatenate(match_index))
        return match_index

    def fix_ch_names(self, verbose=False):
        valid = np.array(['channel', 'channels', 'bipolar_pair', 'bipolar_pairs'])
        label = valid[np.where(np.in1d(valid, np.intersect1d(np.array(self.dims), valid)))][0]
        signal_labels = self[label].data
        format_strings = np.array(list(map(lambda s: s.split(' ')[(-1)].replace('-Ref', '').upper(), np.array(signal_labels))))
        if verbose:
            print('Replacing Old Channel labels with new channel labels')
            display(list(zip(self[label].data, format_strings)))
        self[label].data = format_strings

    def filter_with(self, filter_class, **kwargs):
        """Filter the time series data using the specified filter class.
        Parameters
        ----------
        filter_class : type
            The filter class to use.
        kwargs
            Keyword arguments to pass along to ``filter_class``.
        Returns
        -------
        filtered : TimeSeries
            The resulting data from the filter.
        Raises
        ------
        TypeError
            When ``filter_class`` is not a valid filter class.
        """
        from ptsa.data.filters.base import BaseFilter
        if not issubclass(filter_class, BaseFilter):
            raise TypeError('filter_class must be a child of BaseFilter')
        filtered = filter_class(self, **kwargs).filter()
        return filtered

    def test(self):
        print(self.data)
        print(self.coords)

    def to_mne(self, timeseries, indicator=None):
        from mne import create_info, EpochsArray
        ch_names = list(self.coords['channels'].data)
        info = create_info(ch_names, (self.coords['samplerate'].data), ch_types='eeg')
        from ptsa.data.common import get_axis_index
        data = timeseries.transpose('events', 'channels', 'time')
        mne_evs = np.empty([data['events'].shape[0], 3]).astype(int)
        mne_evs[:, 0] = np.arange(data['events'].shape[0])
        mne_evs[:, 1] = data['time'].shape[0]
        mne_evs[:, 2] = 1
        event_id = dict(event=1)
        if indicator is not None:
            mne_evs[:, 2] = indicator
            event_id = dict(event=1, not_event=0)
        tmin = self.coords['time'].data[0]
        arr = EpochsArray(np.array(data), info, mne_evs, tmin, event_id)
        arr.set_eeg_reference(ref_channels=None)
        arr.apply_proj()
        return arr


if __name__ == '__main__':
    ts = TimeSeriesLF.from_edf('/Users/loganfickling/Clumsy/test_generator.edf')
    ts.test()