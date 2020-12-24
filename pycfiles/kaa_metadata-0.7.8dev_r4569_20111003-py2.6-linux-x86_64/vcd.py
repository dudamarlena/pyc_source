# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/vcd.py
# Compiled at: 2008-10-26 20:23:09
__all__ = [
 'Parser']
import os, core

class VCDFile(core.Collection):
    """
    Parser for VCD files on hard-disc. It parses cue/bin file combinations.
    """
    media = core.MEDIA_DISC

    def __init__(self, file):
        core.Collection.__init__(self)
        self.offset = 0
        self.mime = 'video/vcd'
        self.type = 'vcd video'
        self.parseVCD(file)

    def parseVCD(self, file):
        type = None
        buffer = file.readline(300)
        if not buffer[:6] == 'FILE "':
            raise core.ParseError()
        bin = os.path.join(os.path.dirname(file.name), buffer[6:buffer[6:].find('"') + 6])
        if not os.path.isfile(bin):
            raise core.ParseError()
        f = open(bin, 'rb')
        f.seek(32768, 0)
        buffer = f.read(60000)
        f.close()
        if buffer.find('SVCD') > 0 and buffer.find('TRACKS.SVD') > 0 and buffer.find('ENTRIES.SVD') > 0:
            type = 'SVCD'
        elif buffer.find('INFO.VCD') > 0 and buffer.find('ENTRIES.VCD') > 0:
            type = 'VCD'
        else:
            raise core.ParseError()
        counter = 0
        while 1:
            buffer = file.readline()
            if not len(buffer):
                return
            if buffer[:8] == '  TRACK ':
                counter += 1
                if counter > 1:
                    vi = core.VideoStream()
                    if type == 'VCD':
                        vi.codec = 'MPEG1'
                    else:
                        vi.codec = 'MPEG2'
                    self.tracks.append(vi)

        return


Parser = VCDFile