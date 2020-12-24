# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/pycommon/autoextractors/bandpass_filter.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 3873 bytes
from .filterrecording import FilterRecording
import numpy as np
from scipy import special

class BandpassFilterRecording(FilterRecording):

    def __init__(self, *, recording, freq_min, freq_max, freq_wid):
        FilterRecording.__init__(self, recording=recording, chunk_size=30000)
        self._params = dict(name='bandpass_filter',
          freq_min=freq_min,
          freq_max=freq_max,
          freq_wid=freq_wid)
        self._recording = recording

    def paramsForHash(self):
        return self._params

    def filterChunk(self, *, start_frame, end_frame):
        padding = 3000
        i1 = start_frame - padding
        i2 = end_frame + padding
        padded_chunk = self._read_chunk(i1, i2)
        if i1 < 0:
            for m in range(padded_chunk.shape[0]):
                padded_chunk[m, :-i1] = padded_chunk[(m, -i1)]

        if i2 > self._recording.get_num_frames():
            for m in range(padded_chunk.shape[0]):
                aa = i2 - self._recording.get_num_frames()
                padded_chunk[m, -aa:] = padded_chunk[(m, aa - 1)]

        filtered_padded_chunk = self._do_filter(padded_chunk)
        return filtered_padded_chunk[:, start_frame - i1:end_frame - i1]

    def _create_filter_kernel(self, N, samplerate, freq_min, freq_max, freq_wid=1000):
        T = N / samplerate
        df = 1 / T
        relwid = 3.0
        k_inds = np.arange(0, N)
        k_inds = np.where(k_inds <= (N + 1) / 2, k_inds, k_inds - N)
        fgrid = df * k_inds
        absf = np.abs(fgrid)
        val = np.ones(fgrid.shape)
        if freq_min != 0:
            val = val * (1 + special.erf(relwid * (absf - freq_min) / freq_min)) / 2
            val = np.where(np.abs(k_inds) < 0.1, 0, val)
        if freq_max != 0:
            val = val * (1 - special.erf((absf - freq_max) / freq_wid)) / 2
        val = np.sqrt(val)
        return val

    def _do_filter(self, chunk):
        samplerate = self._recording.get_sampling_frequency()
        M = chunk.shape[0]
        chunk2 = chunk
        chunk_fft = np.fft.rfft(chunk2)
        kernel = self._create_filter_kernel(chunk2.shape[1], samplerate, self._params['freq_min'], self._params['freq_max'], self._params['freq_wid'])
        kernel = kernel[0:chunk_fft.shape[1]]
        chunk_fft = chunk_fft * np.tile(kernel, (M, 1))
        chunk_filtered = np.fft.irfft(chunk_fft)
        return chunk_filtered

    def _read_chunk(self, i1, i2):
        M = len(self._recording.get_channel_ids())
        N = self._recording.get_num_frames()
        if i1 < 0:
            i1b = 0
        else:
            i1b = i1
        if i2 > N:
            i2b = N
        else:
            i2b = i2
        ret = np.zeros((M, i2 - i1))
        ret[:, i1b - i1:i2b - i1] = self._recording.get_traces(start_frame=i1b, end_frame=i2b)
        return ret


def bandpass_filter(recording, freq_min=300, freq_max=6000, freq_wid=1000, resample=None):
    return BandpassFilterRecording(recording=recording,
      freq_min=freq_min,
      freq_max=freq_max,
      freq_wid=freq_wid)