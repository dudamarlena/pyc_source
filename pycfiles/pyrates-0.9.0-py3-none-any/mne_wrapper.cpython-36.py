# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\utility\mne_wrapper.py
# Compiled at: 2019-07-12 12:51:27
# Size of source mod 2**32: 11427 bytes
"""Provides functions to build MNE objects (raw, epoch, evoked) from PyRates simulation results (csv) or from circuit
objects.
"""
import numpy as np
from typing import Union, Optional, List, Any
from pandas import DataFrame
__author__ = 'Richard Gast'
__status__ = 'Development'

def mne_from_dataframe(sim_results: DataFrame, ch_types: Union[(str, List[str])]='eeg', ch_names: Optional[Union[(str, List[str])]]=None, events: Optional[np.ndarray]=None, event_keys: Optional[List[str]]=None, epoch_start: Optional[float]=None, epoch_end: Optional[float]=None, epoch_duration: Optional[float]=None, epoch_averaging: bool=False) -> Any:
    """Uses the data stored on a circuit to create a raw/epoch/evoked mne object.

    Parameters
    ----------
    sim_results
        Pandas dataframe in which circuit simulation results are stored (output of circuit's `run` function).
    ch_types
        Type of the channels, the observation time-series of the observers refer to.
    ch_names
        Name of each channel/observation time-series.
    events
        2D array defining events during the simulation. For a more detailed documentation, see the docstring for
        parameter `events` of :class:`mne.Epochs`.
    event_keys
        Names of the events. For a more detailed documentation, see the docstring for parameter `event_id` of
        :class:`mne.Epochs`.
    epoch_start
        Time, relative to event onset, at which an epoch should start [unit = s]. For a more detailed documentation,
        see the docstring for parameter `tmin` of :class:`mne.Epochs`.
    epoch_end
        Time, relative to event onset, at which an epoch should end [unit = s]. For a more detailed documentation,
        see the docstring for parameter `tmax` of :class:`mne.Epochs`.
    epoch_duration
        Instead of passing `events`, this parameter can be used to create epochs with a fixed duration [unit = s].
        If this is used, do not pass `epoch_start` or `epoch_end`. For a more detailed documentation,
        see the docstring for parameter `duration` of :function:`mne.make_fixed_length_events`.
    epoch_averaging
        Only relevant, if `events` or `event_duration` were passede. If true, an :class:`mne.EvokedArray` instance will
        be returned that contains ttime-series averaged over all epochs.

    Returns
    -------
    Any
        MNE object that contains either the raw, epoched, or averaged (over epochs) data.

    """
    import mne
    dt = sim_results.index[1] - sim_results.index[0]
    if not ch_names:
        ch_names = list(sim_results.keys())
    if type(ch_types) is str:
        ch_types = [ch_types for _ in range(len(ch_names))]
    ch_names_str = []
    for name in ch_names:
        ch_names_str.append(str(name))

    if not epoch_start:
        epoch_start = -0.2 if not epoch_duration else 0.0
    elif not epoch_end:
        epoch_end = 0.5 if not epoch_duration else epoch_duration - 1 / dt
    else:
        info = mne.create_info(ch_names=ch_names_str, ch_types=ch_types, sfreq=(1 / dt))
        raw = mne.io.RawArray(data=(sim_results[ch_names].values.T), info=info)
        if events is not None or epoch_duration:
            if events is None:
                events = mne.make_fixed_length_events(raw=raw, id=0, duration=epoch_duration)
            if not event_keys:
                event_keys = dict()
                for event in np.unique(events[:, 2]):
                    event_keys['event_' + str(event)] = event

            mne_object = mne.Epochs(raw=raw, events=events, event_id=event_keys, tmin=epoch_start, tmax=epoch_end)
            if epoch_averaging:
                data = mne_object.get_data()
                n_epochs = len(data)
                data = np.mean(data, axis=0)
                mne_object = mne.EvokedArray(data=data, info=info, tmin=epoch_start, comment=(event_keys['event_0']), nave=n_epochs)
        else:
            mne_object = raw
    return mne_object


def mne_from_csv(csv_dir: str, ch_types: Union[(str, List[str])]='eeg', ch_names: Optional[Union[(str, List[str])]]=None, events: Optional[np.ndarray]=None, event_keys: Optional[List[str]]=None, epoch_start: Optional[float]=None, epoch_end: Optional[float]=None, epoch_duration: Optional[float]=None, epoch_averaging: bool=False) -> Any:
    """Uses the data stored on circuit to create a raw/epoch/evoked mne object.

    Parameters
    ----------
    csv_dir
        Full path + filename of the csv file that contains the circuit outputs from which an MNE object should be
        created.
    ch_types
        Type of the channels, the observation time-series of the observers refer to.
    ch_names
        Name of each channel/observation time-series.
    events
        2D array defining events during the simulation. For a more detailed documentation, see the docstring for
        parameter `events` of :class:`mne.Epochs`.
    event_keys
        Names of the events. For a more detailed documentation, see the docstring for parameter `event_id` of
        :class:`mne.Epochs`.
    epoch_start
        Time, relative to event onset, at which an epoch should start [unit = s]. For a more detailed documentation,
        see the docstring for parameter `tmin` of :class:`mne.Epochs`.
    epoch_end
        Time, relative to event onset, at which an epoch should end [unit = s]. For a more detailed documentation,
        see the docstring for parameter `tmax` of :class:`mne.Epochs`.
    epoch_duration
        Instead of passing `events`, this parameter can be used to create epochs with a fixed duration [unit = s].
        If this is used, do not pass `epoch_start` or `epoch_end`. For a more detailed documentation,
        see the docstring for parameter `duration` of :function:`mne.make_fixed_length_events`.
    epoch_averaging
        Only relevant, if `events` or `event_duration` were passede. If true, an :class:`mne.EvokedArray` instance will
        be returned that contains ttime-series averaged over all epochs.

    Returns
    -------
    Any
        MNE object that contains either the raw, epoched, or averaged (over epochs) data.

    """
    import mne
    from pandas.io.parsers import read_csv
    output = read_csv(csv_dir, delim_whitespace=True, header=0)
    states = output.values
    sfreq = states[(-1, 0)] / states.shape[0]
    states = states[:, 1:]
    n_channels = states.shape[1]
    if type(ch_types) is str:
        ch_types = [ch_types for _ in range(n_channels)]
    if not ch_names:
        ch_names = output.keys()
        ch_names.pop(0)
    if not epoch_start:
        epoch_start = -0.2 if not epoch_duration else 0.0
    elif not epoch_end:
        epoch_end = 0.5 if not epoch_duration else epoch_duration - 1 / sfreq
    else:
        info = mne.create_info(ch_names=ch_names, ch_types=ch_types, sfreq=sfreq)
        raw = mne.io.RawArray(data=(states.T), info=info)
        if events is not None or epoch_duration:
            if events is None:
                events = mne.make_fixed_length_events(raw=raw, id=0, duration=epoch_duration)
            if not event_keys:
                event_keys = dict()
                for event in np.unique(events[:, 2]):
                    event_keys['event_' + str(event)] = event

            mne_object = mne.Epochs(raw=raw, events=events, event_id=event_keys, tmin=epoch_start, tmax=epoch_end)
            if epoch_averaging:
                data = mne_object.get_data()
                n_epochs = len(data)
                data = np.mean(data, axis=0)
                mne_object = mne.EvokedArray(data=data, info=info, tmin=epoch_start, comment=(event_keys['event_0']), nave=n_epochs)
        else:
            mne_object = raw
    return mne_object