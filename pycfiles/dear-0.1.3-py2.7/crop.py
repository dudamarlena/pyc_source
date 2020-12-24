# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dear/crop.py
# Compiled at: 2012-05-02 04:33:42
import numpy as np
from dear.spectrum import DFTPowerSpectrum

def crop_mmag(audio, start=0, end=None, length=30):
    if end is None:
        end = audio.duration
    end = end <= audio.duration and end or audio.duration
    assert 0 <= start < end
    assert 0 < length
    if end - start <= length:
        return (start, end)
    else:
        win = 512
        time_hop = float(win) / audio.samplerate
        max_mag = 0
        cur_mag = 0
        mag_arr = [0]
        now = start
        new_end = start + length
        for samples in audio.walk(win=win, step=win, start=start, end=end, join_channels=True):
            now += time_hop
            mag = np.sum(np.abs(samples))
            mag_arr.append(mag)
            if now > new_end:
                cur_mag += mag - mag_arr.pop(0)
                if cur_mag > max_mag:
                    new_end = now
                    max_mag = cur_mag
            else:
                cur_mag += mag
                max_mag = cur_mag

        return (int(new_end - length), int(new_end))


def crop_mpwg(audio, start=0, end=None, length=30):
    if end is None:
        end = audio.duration
    end = end <= audio.duration and end or audio.duration
    assert 0 <= start < end
    assert 0 < length
    if end - start <= length:
        return (start, end)
    else:
        win = 512
        time_hop = float(win) / audio.samplerate
        max_mag = 0
        cur_mag = 0
        mag_arr = [0]
        now = start
        new_end = start + length
        spec = DFTPowerSpectrum(audio)
        for frame in spec.walk(win=win, step=win, start=start, end=end, join_channels=True):
            now += time_hop
            mag = np.sum(frame)
            mag_arr.append(mag)
            if now > new_end:
                cur_mag += mag - mag_arr.pop(0)
                if cur_mag > max_mag:
                    new_end = now
                    max_mag = cur_mag
            else:
                cur_mag += mag
                max_mag = cur_mag

        return (
         int(new_end - length), int(new_end))


CROP_ALGORITHMS = {'mmag': crop_mmag, 
   'mpwg': crop_mpwg}
if __name__ == '__main__':
    import getopt, sys, traceback, os, subprocess

    def exit_with_usage():
        print "Usage: $ python -m dear.crop <options>\nOptions:\n     -i         input path\n     -o         output path\n    [-l]        length of clip, default 30 seconds.\n    [-s]        start time in second, defaute 0\n    [-t]        end time, default is duration of song\n    [-a]        algorithm, could be one of ('mmag','mpwg'), default 'mmag'\n    [-r]        samplerate, default 22050\n    [-b]        bitrate, default 64k(bit)\n    [-d]        dim seconds of begining and ending, default 4\n    [--ffmpeg]  specify the path of ffmpeg executable, default 'ffmpeg'\n    [--sox]     specify the path of sox executable, default 'sox'\n"
        exit()


    def print_exc():
        print '-' * 72
        traceback.print_exc()
        print '-' * 72


    if len(sys.argv) < 4:
        exit_with_usage()
    try:
        inputf = None
        output = None
        length = 30
        start = 0
        end = None
        algorithm = 'mmag'
        samplerate = 22050
        bitrate = '64k'
        do_crop = True
        dim = 4
        FFMPEG = 'ffmpeg'
        SOX = 'sox'
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:l:s:t:a:r:b:d:', ('ffmpeg=',
                                                                        'sox='))
        for o, a in opts:
            if o == '-i':
                inputf = a
            elif o == '-o':
                output = a
            elif o == '-l':
                length = int(a)
            elif o == '-s':
                start = int(a)
            elif o == '-t':
                end = int(a)
            elif o == '-a':
                algorithm = a
            elif o == '-r':
                samplerate = int(a)
            elif o == '-b':
                bitrate = a
            elif o == '-d':
                dim = int(a)
            elif o == '--ffmpeg':
                FFMPEG = a
            elif o == '--sox':
                SOX = a

        assert os.path.isfile(inputf)
        assert output is not None
        assert algorithm in CROP_ALGORITHMS
        assert 0 < length
        assert end is None or 0 <= start < end
        assert 0 < samplerate
        assert 0 < bitrate
    except Exception as ex:
        print_exc()
        exit_with_usage()

    if len(args) != 0:
        exit_with_usage()
    func = CROP_ALGORITHMS.get(algorithm)
    import dear.io as io
    decoder = io.get_decoder(name='audioread')
    audio = decoder.Audio(inputf)
    print 'SampleRate: %d Hz\nChannel(s): %d\nDuration: %d sec' % (
     audio.samplerate, audio.channels, audio.duration)
    if start >= audio.duration:
        print '[error] Start time is beyond song duration. Not cropping.'
    else:
        start, end = func(audio, start, end, length)
    duration = end - start
    print start, end, duration
    tmpfile = output + '.crop.tmp.wav'
    cmd = [FFMPEG, '-i', inputf, '-ss', str(start), '-t', str(duration),
     '-ac', '1', '-ar', str(samplerate), '-ab', bitrate,
     tmpfile]
    p = subprocess.Popen(cmd)
    p.wait()
    if dim > 0 and duration > 2 * dim:
        cmd = [
         SOX, tmpfile, output, 'fade', 'p', str(dim),
         str(duration - 1), str(dim)]
        p = subprocess.Popen(cmd)
        p.wait()
    else:
        p = subprocess.Popen(['mv', tmpfile, output])
        p.wait()
    os.remove(tmpfile)