# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dear/io/_io_base.py
# Compiled at: 2012-04-27 00:49:21
import os

class AudioBase(object):
    """"""

    def __init__(self, path):
        """"""
        self._path = path
        if not os.path.isfile(path):
            raise ValueError("`%s' is not a file." % path)

    @property
    def path(self):
        return self._path

    @property
    def samplerate(self):
        """Get sample rate."""
        raise NotImplementedError

    @property
    def channels(self):
        """Get number of channels."""
        raise NotImplementedError

    @property
    def duration(self):
        """Get duration in seconds."""
        raise NotImplementedError

    def __len__(self):
        return self.duration

    def walk(self, win, step, start, end, join_channels):
        """Generator that walks through the audio."""
        raise NotImplementedError