# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/disc/data.py
# Compiled at: 2007-05-07 17:47:54
__all__ = [
 'Parser']
import core

class DataDisc(core.Disc):

    def __init__(self, device):
        core.Disc.__init__(self)
        if self.is_disc(device) != 2:
            raise core.ParseError()
        self.offset = 0
        self.mime = 'unknown/unknown'
        self.type = 'CD'
        self.subtype = 'data'


Parser = DataDisc