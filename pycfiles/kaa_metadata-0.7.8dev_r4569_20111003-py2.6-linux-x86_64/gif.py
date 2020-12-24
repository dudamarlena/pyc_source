# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/image/gif.py
# Compiled at: 2009-05-14 14:51:42
__all__ = [
 'Parser']
import struct, logging, core
log = logging.getLogger('metadata')

class GIF(core.Image):

    def __init__(self, file):
        core.Image.__init__(self)
        self.mime = 'image/gif'
        try:
            header = struct.unpack('<6sHH', file.read(10))
        except struct.error:
            raise core.ParseError()

        (gifType, self.width, self.height) = header
        if not gifType.startswith('GIF'):
            raise core.ParseError()
        self.type = gifType.lower()


Parser = GIF