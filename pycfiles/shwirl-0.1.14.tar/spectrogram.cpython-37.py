# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/spectrogram.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 2100 bytes
import numpy as np
from .image import ImageVisual
from util.fourier import stft, fft_freqs
from ext.six import string_types

class SpectrogramVisual(ImageVisual):
    __doc__ = "Calculate and show a spectrogram\n\n    Parameters\n    ----------\n    x : array-like\n        1D signal to operate on. ``If len(x) < n_fft``, x will be\n        zero-padded to length ``n_fft``.\n    n_fft : int\n        Number of FFT points. Much faster for powers of two.\n    step : int | None\n        Step size between calculations. If None, ``n_fft // 2``\n        will be used.\n    fs : float\n        The sample rate of the data.\n    window : str | None\n        Window function to use. Can be ``'hann'`` for Hann window, or None\n        for no windowing.\n    color_scale : {'linear', 'log'}\n        Scale to apply to the result of the STFT.\n        ``'log'`` will use ``10 * log10(power)``.\n    cmap : str\n        Colormap name.\n    clim : str | tuple\n        Colormap limits. Should be ``'auto'`` or a two-element tuple of\n        min and max values.\n    "

    def __init__(self, x, n_fft=256, step=None, fs=1.0, window='hann', color_scale='log', cmap='cubehelix', clim='auto'):
        self._n_fft = int(n_fft)
        self._fs = float(fs)
        if not isinstance(color_scale, string_types) or color_scale not in ('log',
                                                                            'linear'):
            raise ValueError('color_scale must be "linear" or "log"')
        data = stft(x, self._n_fft, step, self._fs, window)
        data = np.abs(data)
        data = 20 * np.log10(data) if color_scale == 'log' else data
        super(SpectrogramVisual, self).__init__(data, clim=clim, cmap=cmap)

    @property
    def freqs(self):
        """The spectrogram frequencies"""
        return fft_freqs(self._n_fft, self._fs)