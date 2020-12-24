# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/game/spider_man_video.py
# Compiled at: 2009-09-07 17:44:28
"""
Parser for an obscure FMV file format: bin files from the game
"The Amazing Spider-Man vs. The Kingpin" (Sega CD)

Author: Mike Melanson
Creation date: 2006-09-30
File samples: http://samples.mplayerhq.hu/game-formats/spiderman-segacd-bin/
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, UInt32, String, RawBytes
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal

class Chunk(FieldSet):
    __module__ = __name__
    tag_info = {'CONF': ('conf[]', None, 'Configuration header'), 'AUDI': ('audio[]', None, 'Audio chunk'), 'SYNC': ('sync[]', None, 'Start of video frame data'), 'IVRA': ('ivra[]', None, 'Vector codebook (?)'), 'VRAM': ('video[]', None, 'Video RAM tile pattern'), 'CRAM': ('color[]', None, 'Color RAM (palette)'), 'CEND': ('video_end[]', None, 'End of video data'), 'MEND': ('end_file', None, 'End of file')}

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._size = self['length'].value * 8
        fourcc = self['fourcc'].value
        if fourcc in self.tag_info:
            (self._name, self._parser, self._description) = self.tag_info[fourcc]
        else:
            self._parser = None
            self._description = 'Unknown chunk: fourcc %s' % self['fourcc'].display
        return

    def createFields(self):
        yield String(self, 'fourcc', 4, 'FourCC', charset='ASCII')
        yield textHandler(UInt32(self, 'length', 'length'), hexadecimal)
        size = self['length'].value - 8
        if 0 < size:
            if self._parser:
                for field in self._parser(self, size):
                    yield field

            else:
                yield RawBytes(self, 'data', size)


class SpiderManVideoFile(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'spiderman_video', 'category': 'game', 'file_ext': ('bin', ), 'min_size': 8 * 8, 'description': 'The Amazing Spider-Man vs. The Kingpin (Sega CD) FMV video'}
    endian = BIG_ENDIAN

    def validate(self):
        return self.stream.readBytes(0, 4) == 'CONF'

    def createFields(self):
        while not self.eof:
            yield Chunk(self, 'chunk[]')