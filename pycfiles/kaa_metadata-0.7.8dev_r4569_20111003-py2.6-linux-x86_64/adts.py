# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/adts.py
# Compiled at: 2008-10-19 10:01:09
__all__ = [
 'Parser']
import struct, core

class ADTS(core.Music):

    def __init__(self, file):
        core.Music.__init__(self)
        if not file.name.endswith('aac'):
            raise core.ParseError()
        header = struct.unpack('>7B', file.read(7))
        if header[0] != 255 or header[1] >> 4 != 15:
            raise core.ParseError()
        self.mime = 'audio/aac'


Parser = ADTS