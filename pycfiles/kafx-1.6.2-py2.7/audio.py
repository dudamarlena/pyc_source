# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\libs\audio.py
# Compiled at: 2012-05-17 13:06:16
"""This lib contains functions that have to do with audio.

Notes:

Like with the particles, the class Data requires certain amount of stuff
to keep the sync with the video.

1) The method "read" must be called one time for each frame; no more, no less.
2) The frames must be accessed in order.
3) Frames should not be skipped.

Lastly, the use of Data required to have installed ffmpeg and be available
(meaning, to be in the path or the folder of kafx.)

"""
import subprocess, audioop, video

class BPM:

    def __init__(self, fname=None):
        self.start = -1
        self.bpm = -1
        self.fpb = -1
        if fname != None:
            self.OpenBPM(fname)
        return

    def OpenBPM(self, arch):
        """Opens a file specifying the BPM.
                The file mus contain 2 numbers separeted by a comma:
                        the start in ms(milliseconds) of the beat and the BPM(beat per minute.)"""
        f = open(arch, 'r')
        for l in f:
            args = l.split(',')
            if len(args) > 1:
                self.start = video.MSACuadro(int(args[0].strip()))
                self.bpm = float(args[1].strip())

        vi = video.vi
        self.fpb = 60.0 * vi.fps_numerator / vi.fps_denominator / self.bpm

    def BPM(self):
        """Returns a number correlative to the beat.
                1=beat (everything else is not a beat)
                It starts with 0 and grows to 1, then it goes back abruptly to 0 ."""
        if video.cf.framen < self.start:
            return -1
        time = video.cf.framen - self.start
        return time % float(self.fpb) / self.fpb

    def RevBPM(self):
        """Returns a number correlative to the beat.
                1=beat (everything else is not a beat)
                It starts with 1 and decrease until 0 progressively."""
        if video.cf.framen < self.start:
            return -1
        time = video.cf.framen - self.start
        return (self.fpb - time % float(self.fpb)) / self.fpb


class Data:
    proc = None
    frames = ()
    maxint = float(2147483648)

    def __init__(self, archive=None):
        """@The name of the file from which the audio is going to be taken.
                Example: 'myvideo.avi'"""
        self.frameRate = 44100
        self.sampWidth = 4
        self.frameSize = int(self.frameRate / video.vi.fps)
        self.bufSize = self.frameSize * self.sampWidth
        self.args = [
         'ffmpeg', '-loglevel', '3', '-i', archive,
         '-vn', '-acodec', 'pcm_s32le', '-ac', '1', '-ar', str(self.frameRate), '-ab', '32', '-f', 'wav',
         '-y', '-']
        self.proc = subprocess.Popen(self.args, bufsize=self.bufSize, stdout=subprocess.PIPE, stdin=open('audiofakein.txt', 'w'), stderr=open('audioerr.txt', 'w'))

    def __del__(self):
        if self.proc:
            self.proc.terminate()

    def read(self):
        """Reads a line of data, the equivalent to a video frame.
                Is necessary call the function for every frame of video, to archive sync
                 (Example: OnFrameStarts.)"""
        if self.proc:
            self.frames = self.proc.stdout.read(self.bufSize)
        else:
            self.frames = []
        return self.frames

    def rms(self):
        """Returns the RMS(root mean square) for the current data (Is like the power of the sound.)"""
        return audioop.rms(self.frames, self.sampWidth) / self.maxint

    def sample(self, frame):
        """Returns the value of a data.
                @frame : the number of frame from which is required a value
                (must be lower than frameSize)"""
        if frame < len(self.frames):
            return audioop.getsample(self.frames, self.sampWidth, frame) / self.maxint
        else:
            return 0.0