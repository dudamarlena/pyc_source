# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/pcm.py
# Compiled at: 2009-05-14 14:58:47
__all__ = [
 'Parser']
import sndhdr, core

class PCM(core.Music):

    def __init__(self, file):
        core.Music.__init__(self)
        t = self._what(file)
        if not t:
            raise core.ParseError()
        self.type, self.samplerate, self.channels, self.bitrate, self.samplebits = t
        if self.bitrate == -1:
            raise core.ParseError()
        self.mime = 'audio/%s' % self.type

    def _what(self, f):
        """Recognize sound headers"""
        h = f.read(512)
        for tf in sndhdr.tests:
            try:
                res = tf(h, f)
            except IndexError:
                continue

            if res:
                return res

        return


Parser = PCM