# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/mp3.py
# Compiled at: 2011-03-28 15:09:52
import sys
from struct import pack, unpack
stderr = sys.stderr

class MP3Storage:

    def __init__(self, debug=0):
        self.debug = debug
        self.isstereo = None
        self.bit_rate = None
        self.sample_rate = None
        self.initial_skip = 0
        self.frames = []
        self.played_samples = 0
        self.playing_frame = 0
        self.seeksamples = 0
        return

    def __repr__(self):
        return '<MP3Storage: isstereo=%r, bit_rate=%r, sample_rate=%r, initial_skip=%r, frames=%d>' % (
         self.isstereo, self.bit_rate, self.sample_rate, self.initial_skip, len(self.frames))

    def set_stereo(self, isstereo):
        if self.isstereo == None:
            self.isstereo = isstereo
        elif self.isstereo != isstereo:
            print >> stderr, 'mp3: isstereo does not match!'
        return

    def set_bit_rate(self, bit_rate):
        if self.bit_rate == None:
            self.bit_rate = bit_rate
        elif self.bit_rate != bit_rate:
            print >> stderr, 'mp3: bit_rate does not match! (variable bitrate mp3 cannot be used for SWF)'
        return

    def set_sample_rate(self, sample_rate):
        if self.sample_rate == None:
            self.sample_rate = sample_rate
        elif self.sample_rate != sample_rate:
            print >> stderr, 'mp3: sample_rate does not match! (variable bitrate mp3 cannot be used for SWF)'
        return

    def set_initial_skip(self, initial_skip):
        if initial_skip:
            self.initial_skip = initial_skip

    def add_frame(self, nsamples, frame):
        self.frames.append((nsamples, frame))

    def needsamples(self, t):
        return int(self.sample_rate * t) + self.initial_skip

    def get_frames_until(self, t):
        needsamples = self.needsamples(t)
        if needsamples < 0:
            return (0, 0, [])
        nsamples = 0
        frames = []
        while self.playing_frame < len(self.frames):
            (samples, data) = self.frames[self.playing_frame]
            if needsamples <= self.played_samples + nsamples + samples:
                break
            nsamples += samples
            frames.append(data)
            self.playing_frame += 1

        seeksamples = self.seeksamples
        self.played_samples += nsamples
        self.seeksamples = needsamples - self.played_samples
        return (
         nsamples, seeksamples, frames)

    def seek_frame(self, t):
        needsamples = self.needsamples(t)
        self.played_samples = 0
        for (i, (samples, data)) in enumerate(self.frames):
            if needsamples <= self.played_samples + samples:
                break
            self.played_samples += samples
            self.playing_frame = i

        self.seeksamples = needsamples - self.played_samples


class MP3Reader:
    """
  read MPEG frames.
  """

    def __init__(self, storage):
        self.storage = storage

    def read(self, n):
        if self.length != None:
            if self.length <= 0:
                return ''
            self.length -= n
        return self.fp.read(n)

    BIT_RATE = {(1, 1): (0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 0), 
       (1, 2): (0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, 0), 
       (1, 3): (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0), 
       (2, 1): (0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 144, 176, 192, 224, 256, 0), 
       (2, 2): (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0), 
       (2, 3): (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0)}
    SAMPLE_RATE = {3: (44100, 48000, 32000), 
       2: (22050, 24000, 16000), 
       0: (11025, 12000, 8000)}

    def read_mp3file(self, fp, length=None, totalsamples0=None, seeksamples=None, verbose=False):
        """parameter seeksamples is ignored."""
        self.fp = fp
        self.length = length
        totalsamples = 0
        while 1:
            x = self.read(4)
            if len(x) < 4:
                break
            if x.startswith('TAG'):
                data = x[3] + self.read(124)
                if verbose:
                    print >> stderr, 'TAG', repr(data)
                continue
            elif x.startswith('ID3'):
                id3version = x[3] + fp.read(1)
                flags = ord(fp.read(1))
                s = [ ord(c) & 127 for c in fp.read(4) ]
                size = s[0] << 21 | s[1] << 14 | s[2] << 7 | s[3]
                data = fp.read(size)
                if verbose:
                    print >> stderr, 'ID3', repr(data)
                continue
            h = unpack('>L', x)[0]
            if h & 4292870144 != 4292870144:
                continue
            version = (h & 1572864) >> 19
            if version == 1:
                continue
            layer = 4 - ((h & 393216) >> 17)
            if layer == 4:
                continue
            protected = not h & 65536
            b = (h & 61440) >> 12
            if b == 0 or b == 15:
                continue
            s = (h & 3072) >> 10
            if s == 3:
                continue
            if version == 3:
                bit_rate = self.BIT_RATE[(1, layer)][b]
            else:
                bit_rate = self.BIT_RATE[(2, layer)][b]
            self.storage.set_bit_rate(bit_rate)
            sample_rate = self.SAMPLE_RATE[version][s]
            self.storage.set_sample_rate(sample_rate)
            nsamples = 1152
            if sample_rate <= 24000:
                nsamples = 576
            pad = (h & 512) >> 9
            channel = (h & 192) >> 6
            self.storage.set_stereo(1 - channel / 2)
            joint = (h & 48) >> 4
            copyright = bool(h & 8)
            original = bool(h & 4)
            emphasis = h & 3
            if version == 3:
                framesize = 144000 * bit_rate / sample_rate + pad
            else:
                framesize = 72000 * bit_rate / sample_rate + pad
            if protected:
                self.read(2)
            if verbose:
                print >> stderr, 'Frame: bit_rate=%dk, sample_rate=%d, framesize=%d' % (
                 bit_rate, sample_rate, framesize)
            data = x + self.read(framesize - 4)
            self.storage.add_frame(nsamples, data)
            totalsamples += nsamples

        if totalsamples0:
            assert totalsamples == totalsamples0


if __name__ == '__main__':
    s = MP3Storage(True)
    MP3Reader(s).read_mp3file(file(sys.argv[1]), verbose=1)