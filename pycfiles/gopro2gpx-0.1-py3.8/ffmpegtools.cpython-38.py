# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gopro2gpx/ffmpegtools.py
# Compiled at: 2020-04-17 10:36:21
# Size of source mod 2**32: 2216 bytes
import subprocess, re

class FFMpegTools:

    def __init__(self, config):
        self.config = config

    def runCmd(self, cmd, args):
        result = subprocess.run(([cmd] + args), stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
        output = result.stderr.decode('utf-8')
        return output

    def runCmdRaw(self, cmd, args):
        result = subprocess.run(([cmd] + args), stdout=(subprocess.PIPE), stderr=(subprocess.DEVNULL))
        output = result.stdout
        return output

    def getMetadataTrack(self, fname):
        """
        % ffprobe GH010039.MP4 2>&1

        The channel marked as gpmd (Stream #0:3(eng): Data: none (gpmd / 0x646D7067), 29 kb/s (default))
        In this case, the stream #0:3 is the required one (get the 3)

        Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'GH010039.MP4':
            Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 189 kb/s (default)
            Stream #0:2(eng): Data: none (tmcd / 0x64636D74), 0 kb/s (default)
            Stream #0:3(eng): Data: none (gpmd / 0x646D7067), 29 kb/s (default)
            Stream #0:4(eng): Data: none (fdsc / 0x63736466), 12 kb/s (default)
        """
        output = self.runCmd(self.config.ffprobe_cmd, [fname])
        reg = re.compile('Stream #\\d:(\\d)\\(.+\\): Data: \\w+ \\(gpmd', flags=(re.I | re.M))
        m = reg.search(output)
        res = reg.search('Stream #0:2(eng): Data: none (gpmd / 0x646D7067), 29 kb/s (default)')
        print(m)
        print(output)
        if not m:
            return
        return (
         int(m.group(1)), m.group(0))

    def getMetadata(self, track, fname):
        output_file = '-'
        args = ['-y', '-i', fname, '-codec', 'copy', '-map', '0:%d' % track, '-f', 'rawvideo', output_file]
        output = self.runCmdRaw(self.config.ffmpeg_cmd, args)
        return output