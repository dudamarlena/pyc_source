# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\audio\spectrum.py
# Compiled at: 2020-04-22 07:01:34
# Size of source mod 2**32: 1368 bytes
"""
module for audio spectrum analysis
"""
import wave, numpy as np

class FreqAnalysis:
    __doc__ = '\n    spectrum analysis class\n    '

    def __init__(self, file_name: str):
        wav = wave.open(file_name, 'rb')
        n_frames = wav.getnframes()
        self._frame_rate = wav.getframerate()
        self._duration = n_frames / self._frame_rate
        str_data = wav.readframes(n_frames)
        wave_data = np.frombuffer(str_data, dtype=(np.short))
        wave_data.shape = (-1, 1)
        self._wave_data = wave_data.T
        wav.close()

    def spectrum(self, start_offset: int, window: int, cutoff=5000) -> tuple:
        """
        spectrum of the targeted audio segment
        :param start_offset:
        :param window:
        :param cutoff:
        :return:
        """
        total_samples = self._frame_rate * window
        start = start_offset * self._frame_rate
        data_freq = self._frame_rate / (total_samples - 1)
        spec = np.fft.fft(self._wave_data[0][start:start + total_samples])
        max_idx = min(int(cutoff / data_freq), int(len(spec) / 2))
        freq = np.arange(0, max_idx) * data_freq
        return (freq, spec[:max_idx])

    def __str__(self):
        return f"frame_rate: {self._frame_rate}\nduration: {self._duration}"