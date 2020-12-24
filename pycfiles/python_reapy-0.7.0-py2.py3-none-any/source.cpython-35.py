# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/core/item/source.py
# Compiled at: 2019-03-02 09:22:22
# Size of source mod 2**32: 2323 bytes
from reapy import reascript_api as RPR

class Source:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Source)

    @property
    def _args(self):
        return (self.id,)

    def delete(self):
        """
        Delete source. Be sure that no references to source remains.
        """
        RPR.PCM_Source_Destroy(self.id)

    @property
    def filename(self):
        """
        Return source file name.

        Returns
        -------
        filename : str
            Source file name.
        """
        _, filename, _ = RPR.GetMediaSourceFileName(self.id, '', 100000)
        return filename

    @property
    def length(self, unit='seconds'):
        """
        Return source length in `unit`.

        Parameters
        ----------
        unit : {"beats", "seconds"}

        Returns
        -------
        length : float
            Source length in `unit`.
        """
        length, _, is_quantized = RPR.GetMediaSourceLength(self.id, 0)
        if is_quantized:
            if unit == 'beats':
                return length
            if unit == 'seconds':
                raise NotImplementedError
        else:
            if unit == 'beats':
                raise NotImplementedError
            elif unit == 'seconds':
                return length

    @property
    def n_channels(self):
        """
        Return number of channels in source media.

        Returns
        -------
        n_channels : int
            Number of channels in source media.
        """
        n_channels = RPR.GetMediaSourceNumChannels(self.id)
        return n_channels

    @property
    def sample_rate(self):
        """
        Return source sample rate.

        Returns
        -------
        sample_rate : int
            Source sample rate.
        """
        sample_rate = RPR.GetMediaSourceSampleRate(self.id)
        return sample_rate

    @property
    def type(self):
        """
        Return source type ("WAV, "MIDI", etc.).

        Returns
        -------
        type : str
            Source type.
        """
        _, type, _ = RPR.GetMediaSourceType(self.id, '', 100000)
        return type