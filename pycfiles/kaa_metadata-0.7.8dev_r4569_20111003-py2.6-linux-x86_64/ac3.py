# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/ac3.py
# Compiled at: 2008-03-23 12:56:49
__all__ = [
 'Parser']
import struct, core
FSCOD = [
 48000, 44100, 32000, 0]
ACMOD = [
 ('1+1', 2, 'Ch1, Ch2'),
 ('1/0', 1, 'C'),
 ('2/0', 2, 'L, R'),
 ('3/0', 3, 'L, C, R'),
 ('2/1', 3, 'L, R, S'),
 ('3/1', 4, 'L, C, R, S'),
 ('2/2', 4, 'L, R, SL, SR'),
 ('3/2', 5, 'L, C, R, SL, SR')]
FRMSIZCOD = [
 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192,
 224, 256, 320, 384, 448, 512, 576, 640]

class AC3(core.Music):

    def __init__(self, file):
        core.Music.__init__(self)
        if file.name.endswith('.ac3'):
            check_length = 1000
        else:
            check_length = 1
        for i in range(check_length):
            if file.read(2) == '\x0bw':
                break
        else:
            raise core.ParseError()

        info = struct.unpack('<HBBBB', file.read(6))
        self.samplerate = FSCOD[(info[1] >> 6)]
        self.bitrate = FRMSIZCOD[((info[1] & 63) >> 1)] * 1000
        bsmod = info[2] & 7
        channels = ACMOD[(info[3] >> 5)]
        acmod = info[3] >> 5
        self.channels = ACMOD[acmod][1]
        bits = 0
        if acmod & 1 and not acmod == 1:
            bits += 2
        if acmod & 4:
            bits += 2
        if acmod == 2:
            bits += 2
        info = ((info[3] & 31) << 8) + info[4]
        for i in range(13 - bits - 1):
            info = info >> 1

        if info & 1:
            self.channels += 1
        file.seek(-1, 2)
        size = file.tell()
        self.length = size * 8.0 / self.bitrate
        self.codec = 8192
        self.mime = 'audio/ac3'


Parser = AC3