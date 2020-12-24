# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\core\item\source.py
# Compiled at: 2020-05-09 09:40:13
# Size of source mod 2**32: 2824 bytes
import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject

class Source(ReapyObject):

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, Source) and self.id == other.id

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

    @reapy.inside_reaper()
    @property
    def has_valid_id(self):
        """
        Whether ReaScript ID is still valid.

        For instance, if source has been deleted, ID will not be valid
        anymore.

        :type: bool
        """
        pointer, name = self._get_pointer_and_name()
        return any((RPR.ValidatePtr2(project.id, pointer, name) for project in reapy.get_projects()))

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
        elif unit == 'beats':
            raise NotImplementedError
        else:
            if unit == 'seconds':
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