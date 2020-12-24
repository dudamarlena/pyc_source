# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/io/loadmicros.py
# Compiled at: 2018-11-05 17:00:12
# Size of source mod 2**32: 13223 bytes
"""loadmicros.py A script to allow a user to load micro-wire data. Taken from: https://github.com/alafuzof/NeuralynxIO"""
from __future__ import division
import os, warnings, numpy as np, datetime
__all__ = [
 'load_micros']
HEADER_LENGTH = 16384
NCS_SAMPLES_PER_RECORD = 512
NCS_RECORD = np.dtype([('TimeStamp', np.uint64),
 (
  'ChannelNumber', np.uint32),
 (
  'SampleFreq', np.uint32),
 (
  'NumValidSamples', np.uint32),
 (
  'Samples', np.int16, NCS_SAMPLES_PER_RECORD)])
NEV_RECORD = np.dtype([('stx', np.int16),
 (
  'pkt_id', np.int16),
 (
  'pkt_data_size', np.int16),
 (
  'TimeStamp', np.uint64),
 (
  'event_id', np.int16),
 (
  'ttl', np.int16),
 (
  'crc', np.int16),
 (
  'dummy1', np.int16),
 (
  'dummy2', np.int16),
 (
  'Extra', np.int32, 8),
 ('EventString', 'S', 128)])
VOLT_SCALING = (1, 'V')
MILLIVOLT_SCALING = (1000, 'mV')
MICROVOLT_SCALING = (1000000, 'µV')

def load_ncs(file_path, load_time=True, rescale_data=True, signal_scaling='mv'):
    """Loads file as a Neuralynx (.ncs) continuous acquisition file and extract the content.

    Parameters
    ----------
    file_path: str, ending in .ncs
    load_time: bool, by default True, calculates the sample time points
    rescale_data: bool, by default True, whether or not to scale the signal to signal_scaling
    signal_scaling: str, must be:
                'mv' for milli-volts
                'uV' or 'µV' for micro-volts
                'V' for volts

    Returns
    -------
    ncs: array like object containing data
    """
    global MICROVOLT_SCALING
    global MILLIVOLT_SCALING
    global VOLT_SCALING
    if signal_scaling in ('mv', 'mv'):
        signal_scaling = MILLIVOLT_SCALING
    else:
        if signal_scaling in ('uV', 'µV', 'uV', 'µV'):
            signal_scaling = MICROVOLT_SCALING
        else:
            if signal_scaling in ('V', 'V'):
                signal_scaling = VOLT_SCALING
            else:
                raise TypeError('inputted scale could not be understood')
    file_path = os.path.abspath(file_path)
    with open(file_path, 'rb') as (fid):
        raw_header = read_header(fid)
        records = read_records(fid, NCS_RECORD)
    header = parse_header(raw_header)
    check_ncs_records(records)
    data = records['Samples'].ravel()
    if rescale_data:
        try:
            data = data.astype(np.float64) * (np.float64(header['ADBitVolts']) * signal_scaling[0])
        except KeyError:
            warnings.warn('Unable to rescale data, no ADBitVolts value specified in header')
            rescale_data = False

    ncs = dict()
    ncs['file_path'] = file_path
    ncs['raw_header'] = raw_header
    ncs['header'] = header
    ncs['data'] = data
    ncs['data_units'] = signal_scaling[1] if rescale_data else 'ADC counts'
    ncs['sampling_rate'] = records['SampleFreq'][0]
    ncs['channel_number'] = records['ChannelNumber'][0]
    ncs['timestamp'] = records['TimeStamp']
    if load_time:
        num_samples = data.shape[0]
        times = np.interp(np.arange(num_samples), np.arange(0, num_samples, 512), records['TimeStamp']).astype(np.uint64)
        ncs['time'] = times
        ncs['time_units'] = 'µs'
    try:
        assert float(ncs['header']['SamplingFrequency']) == 1000000.0 / (np.unique(np.diff(ncs['timestamp'])) / 512.0)
    except AssertionError as e:
        try:
            print(e)
        finally:
            e = None
            del e

    return ncs


def read_header(fid):
    """Reads the header of the file

    Parameters
    ----------
    fid: path to the file

    Returns
    -------
    raw_hdr: object, header file for Neural Lynx
    """
    pos = fid.tell()
    fid.seek(0)
    raw_hdr = fid.read(HEADER_LENGTH).strip(b'\x00')
    fid.seek(pos)
    return raw_hdr


def parse_header(raw_hdr):
    """

    Parameters
    ----------
    raw_hdr

    Returns
    -------

    """
    hdr = dict()
    raw_hdr = raw_hdr.decode('iso-8859-1')
    hdr_lines = [line.strip() for line in raw_hdr.split('\r\n') if line != '']
    if hdr_lines[0] != '######## Neuralynx Data File Header':
        warnings.warn('Unexpected start to header: ' + hdr_lines[0])
    try:
        assert hdr_lines[1].split()[1:3] == ['File', 'Name']
        hdr['FileName'] = ' '.join(hdr_lines[1].split()[3:])
    except:
        warnings.warn('Unable to parse original file path from Neuralynx header: ' + hdr_lines[1])

    hdr['TimeOpened'] = hdr_lines[2][3:]
    hdr['TimeOpened_dt'] = parse_neuralynx_time_string(hdr_lines[2])
    hdr['TimeClosed'] = hdr_lines[3][3:]
    hdr['TimeClosed_dt'] = parse_neuralynx_time_string(hdr_lines[3])
    for line in hdr_lines[4:]:
        try:
            name, value = line[1:].split()
            hdr[name] = value
        except:
            warnings.warn('Unable to parse parameter line from Neuralynx header: ' + line)

    return hdr


def read_records(fid, record_dtype, record_skip=0, count=None):
    """

    Parameters
    ----------
    fid
    record_dtype
    record_skip
    count

    Returns
    -------

    """
    if count is None:
        count = -1
    pos = fid.tell()
    fid.seek(HEADER_LENGTH, 0)
    fid.seek(record_skip * record_dtype.itemsize, 1)
    rec = np.fromfile(fid, record_dtype, count=count)
    fid.seek(pos)
    return rec


def estimate_record_count(file_path, record_dtype):
    """

    Parameters
    ----------
    file_path
    record_dtype

    Returns
    -------

    """
    file_size = os.path.getsize(file_path)
    file_size -= HEADER_LENGTH
    if file_size % record_dtype.itemsize != 0:
        warnings.warn('File size is not divisible by record size (some bytes unaccounted for)')
    return file_size / record_dtype.itemsize


def parse_neuralynx_time_string(time_string):
    """

    Parameters
    ----------
    time_string

    Returns
    -------

    """
    try:
        tmp_date = [int(x) for x in time_string.split()[4].split('/')]
        tmp_time = [int(x) for x in time_string.split()[(-1)].replace('.', ':').split(':')]
        tmp_microsecond = tmp_time[3] * 1000
    except:
        warnings.warn('Unable to parse time string from Neuralynx header: ' + time_string)
        return
        return datetime.datetime(tmp_date[2], tmp_date[0], tmp_date[1], tmp_time[0], tmp_time[1], tmp_time[2], tmp_microsecond)


def check_ncs_records(records):
    """

    Parameters
    ----------
    records : nd.array

    Returns
    -------

    """
    dt = np.diff(records['TimeStamp'])
    dt = np.abs(dt - dt[0])
    if not np.all(records['ChannelNumber'] == records[0]['ChannelNumber']):
        warnings.warn('Channel number changed during record sequence')
        return False
    if not np.all(records['SampleFreq'] == records[0]['SampleFreq']):
        warnings.warn('Sampling frequency changed during record sequence')
        return False
    if not np.all(records['NumValidSamples'] == 512):
        warnings.warn('Invalid samples in one or more records')
        return False
    if not np.all(dt <= 1):
        warnings.warn('Time stamp difference tolerance exceeded')
        return False
    return True


def load_nev(file_path):
    """

    Parameters
    ----------
    file_path

    Returns
    -------

    """
    file_path = os.path.abspath(file_path)
    with open(file_path, 'rb') as (fid):
        raw_header = read_header(fid)
        records = read_records(fid, NEV_RECORD)
    header = parse_header(raw_header)
    nev = dict()
    nev['file_path'] = file_path
    nev['raw_header'] = raw_header
    nev['header'] = header
    nev['records'] = records
    nev['events'] = records[['pkt_id', 'TimeStamp', 'event_id', 'ttl', 'Extra', 'EventString']]
    return nev


def load_micros(filepath):
    """

    Parameters
    ----------
    filepath: str, ending in .ncs
              path to neuralynx cheetah file

    Returns
    -------
    TimeSeries object containing requested data
    """
    from Clumsy import TimeSeriesLF
    ncs = load_ncs(filepath)
    ts = TimeSeriesLF(data=(ncs['data']), dims=[
     'time'],
      coords={'samplerate':ncs['header']['SamplingFrequency'], 
     'time':ncs['time'], 
     'channel':ncs['header']['AcqEntName']})
    return ts


if __name__ == '__main__':
    from ptsa.data.timeseries import TimeSeries
    path = '/data/eeg/TJ035/raw/2011-12-21/nlx/CSC1.ncs'
    ncs = load_ncs(path)
    ts = TimeSeries(data=(ncs['data']), dims=[
     'time'],
      coords={'samplerate':ncs['header']['SamplingFrequency'], 
     'time':ncs['time'], 
     'channel':ncs['header']['AcqEntName']})