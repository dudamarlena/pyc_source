# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImageMode.py
# Compiled at: 2007-09-25 20:00:35
_modes = {}

class ModeDescriptor:

    def __init__(self, mode, bands, basemode, basetype):
        self.mode = mode
        self.bands = bands
        self.basemode = basemode
        self.basetype = basetype

    def __str__(self):
        return self.mode


def getmode(mode):
    if not _modes:
        import Image
        for (m, (basemode, basetype, bands)) in Image._MODEINFO.items():
            _modes[m] = ModeDescriptor(m, bands, basemode, basetype)

        _modes['LA'] = ModeDescriptor('LA', ('L', 'A'), 'L', 'L')
        _modes['PA'] = ModeDescriptor('PA', ('P', 'A'), 'RGB', 'L')
    return _modes[mode]