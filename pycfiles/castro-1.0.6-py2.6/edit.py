# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/edit.py
# Compiled at: 2011-03-28 15:09:52
import sys, re
from movie import SWFInfo, MovieContainer
from output import FLVVideoStream, MPEGVideoStream, SWFVideoStream, SWFShapeStream, ImageSequenceStream, MovieBuilder
stderr = sys.stderr

class RangeError(ValueError):
    pass


def range2list(s, n0, n1, step=1):
    PAT_RANGE = re.compile('^([0-9]*)-([0-9]*)$')
    r = []
    for i in s.split(','):
        i = i.strip()
        if not i:
            continue
        if i.isdigit():
            n = int(i)
            if n0 <= n and n <= n1:
                r.append(n)
            else:
                raise RangeError('%d: must be in %d...%d' % (n, n0, n1))
        else:
            m = PAT_RANGE.match(i.strip())
            if not m:
                raise RangeError('%r: illegal number' % i)
            b = n0
            if m.group(1):
                b = int(m.group(1))
            e = n1
            if m.group(2):
                e = int(m.group(2))
            if e < b:
                b, e = e, b
            if b < n0:
                raise RangeError('%d: must be in %d...%d' % (b, n0, n1))
            if n1 < e:
                raise RangeError('%d: must be in %d...%d' % (e, n0, n1))
            r.extend(xrange(b, e + 1, step))

    return r


def reorganize(info, stream, moviefiles, range_str='-', loop=True, seekbar=True, step=1, kfinterval=0, mp3seek=True, mp3skip=0, debug=0):
    movie = MovieContainer(info)
    for fname in moviefiles:
        if fname.endswith('.swf'):
            movie.parse_vnc2swf(fname, True, debug=debug)
        elif fname.endswith('.flv'):
            movie.parse_flv(fname, True, debug=debug)
        elif fname.endswith('.vnc'):
            movie.parse_vncrec(fname, debug=debug)
        else:
            raise ValueError('unsupported format: %r' % fname)

    r = range2list(range_str, 0, movie.nframes - 1, step)
    if movie.info.mp3:
        if isinstance(mp3skip, float):
            mp3skip = int(mp3skip * movie.info.mp3.sample_rate)
        movie.info.mp3.set_initial_skip(mp3skip)
    builder = MovieBuilder(movie, stream, mp3seek=mp3seek, kfinterval=kfinterval, debug=debug)
    builder.build(r)
    stream.close()
    movie.info.write_html(seekbar=seekbar, loop=loop)
    return 0


def main(argv):
    import getopt

    def usage():
        print >> stderr, 'usage: %s\n    [-d] [-c] [-t type] [-f|-F frames] [-a mp3file] [-r framerate]\n    [-S mp3sampleskip] [-C WxH+X+Y] [-B blocksize] [-K keyframe]\n    [-R framestep] [-s scaling]\n    -o outfile.swf file1 file2 ...\n\n    Specify one output filename from the following:\n      *.swf: generate a SWF movie.\n      *.flv: generate a FLV movie.\n      *.mpg: generate a MPEG movie.\n      *.png|*.bmp: save snapshots of given frames as "X-nnn.png"\n      \n    -d: debug mode.\n    -c: compression.\n    -t {swf5,swf7,flv,mpeg,png,bmp}: specify the output movie type.\n    -f(-F) frames: frames to extract. e.g. 1-2,100-300,310,500-\n       -F disables seeking audio.\n    -R framestep: frame resampling step (default: 1)\n    -s scaling: scale factor (default: 1.0)\n    -a filename: attach MP3 file(s). (multiple files can be specified)\n    -r framerate: override framerate.\n    -B blocksize: (SWF7 and FLV mode only) blocksize of video packet (must be a multiple of 16)\n    -K keyframe: keyframe interval\n    -S N[s]: skip the first N samples (or N seconds) of the sound when the movie starts.\n    -C WxH+X+Y: crop a specific area of the movie.\n    -b: disable seekbar.\n    -l: disable loop.\n    -z: make the movie scalable.\n    ' % argv[0]
        return 100

    try:
        (opts, args) = getopt.getopt(argv[1:], 'dr:o:t:cHa:S:C:B:K:f:F:R:s:blz')
    except getopt.GetoptError:
        return usage()
    else:
        debug = 0
        info = SWFInfo()
        range_str = '-'
        step = 1
        streamtype = None
        kfinterval = 0
        mp3skip = 0
        mp3seek = True
        loop = True
        seekbar = True
        for (k, v) in opts:
            if k == '-d':
                debug += 1
            elif k == '-r':
                info.set_framerate(float(v))
            elif k == '-o':
                info.filename = v
            elif k == '-t':
                v = v.lower()
                if v not in ('swf5', 'swf7', 'mpeg', 'mpg', 'flv', 'png', 'bmp', 'gif'):
                    print >> stderr, 'Invalid output type:', v
                    return usage()
                streamtype = v
            elif k == '-a':
                fp = file(v, 'rb')
                print >> stderr, 'Reading mp3 file: %s...' % v
                info.reg_mp3blocks(fp)
                fp.close()
            elif k == '-S':
                if v.endswith('s'):
                    mp3skip = float(v[:-1])
                else:
                    mp3skip = int(v)
            elif k == '-C':
                try:
                    info.set_clipping(v)
                except ValueError:
                    print >> stderr, 'Invalid clipping specification:', v
                    return usage()

            elif k == '-B':
                blocksize = int(v)
                assert 0 < blocksize and blocksize <= 256 and blocksize % 16 == 0, 'Invalid block size.'
                info.blocksize = blocksize
            elif k == '-K':
                kfinterval = int(v)
            elif k == '-c':
                info.compression = True
            elif k == '-f':
                range_str = v
            elif k == '-F':
                range_str = v
                mp3seek = False
            elif k == '-R':
                step = int(v)
                mp3seek = False
            elif k == '-s':
                info.scaling = float(v)
                assert 0 < info.scaling and info.scaling <= 1.0, 'Invalid scaling.'
            elif k == '-b':
                seekbar = False
            elif k == '-l':
                loop = False
            elif k == '-z':
                info.set_scalable(True)

    if not args:
        print >> stderr, 'Specify at least one input movie.'
        return usage()
    else:
        if not info.filename:
            print >> stderr, 'Specify exactly one output file.'
            return usage()
        if not streamtype:
            v = info.filename
            if v.endswith('.swf'):
                streamtype = 'swf5'
            elif v.endswith('.png'):
                streamtype = 'png'
            elif v.endswith('.bmp'):
                streamtype = 'bmp'
            elif v.endswith('.gif'):
                streamtype = 'gif'
            elif v.endswith('.mpg') or v.endswith('.mpeg'):
                streamtype = 'mpeg'
            elif v.endswith('.flv'):
                streamtype = 'flv'
            else:
                print >> stderr, 'Unknown stream type.'
                return 100
        if streamtype == 'mpeg' and not MPEGVideoStream:
            print >> stderr, 'MPEGVideoStream is not supported.'
            return 100
        stream = None
        if streamtype == 'swf5':
            stream = SWFShapeStream(info, debug=debug)
        elif streamtype == 'swf7':
            stream = SWFVideoStream(info, debug=debug)
        elif streamtype in ('mpg', 'mpeg'):
            stream = MPEGVideoStream(info, debug=debug)
        elif streamtype == 'flv':
            stream = FLVVideoStream(info, debug=debug)
        else:
            stream = ImageSequenceStream(info, debug=debug)
        try:
            return reorganize(info, stream, args, range_str, loop=loop, seekbar=seekbar, step=step, kfinterval=kfinterval, mp3seek=mp3seek, mp3skip=mp3skip, debug=debug)
        except RangeError, e:
            print >> stderr, 'RangeError:', e
            return 100

        return


if __name__ == '__main__':
    sys.exit(main(sys.argv))