# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/riff.py
# Compiled at: 2010-08-22 17:18:17
__all__ = [
 'Parser']
import os, struct, string, logging, time, core
log = logging.getLogger('metadata')
AVIINFO = {'INAM': 'title', 
   'IART': 'artist', 
   'IPRD': 'product', 
   'ISFT': 'software', 
   'ICMT': 'comment', 
   'ILNG': 'language', 
   'IKEY': 'keywords', 
   'IPRT': 'trackno', 
   'IFRM': 'trackof', 
   'IPRO': 'producer', 
   'IWRI': 'writer', 
   'IGNR': 'genre', 
   'ICOP': 'copyright'}
PIXEL_ASPECT = {1: (
     1, 1), 
   2: (
     12, 11), 
   3: (
     10, 11), 
   4: (
     16, 11), 
   5: (
     40, 33)}

class Riff(core.AVContainer):
    """
    AVI parser also parsing metadata like title, languages, etc.
    """
    table_mapping = {'AVIINFO': AVIINFO}

    def __init__(self, file):
        core.AVContainer.__init__(self)
        h = file.read(12)
        if h[:4] != 'RIFF' and h[:4] != 'SDSS':
            raise core.ParseError()
        self.has_idx = False
        self.header = {}
        self.junkStart = None
        self.infoStart = None
        self.type = h[8:12]
        if self.type == 'AVI ':
            self.mime = 'video/avi'
        else:
            if self.type == 'WAVE':
                self.mime = 'audio/wav'
            try:
                while self._parseRIFFChunk(file):
                    pass

            except IOError:
                log.exception('error in file, stop parsing')

        self._find_subtitles(file.name)
        if not self.has_idx and self.media == core.MEDIA_AV:
            log.debug('WARNING: avi has no index')
            self._set('corrupt', True)
        return

    def _find_subtitles(self, filename):
        """
        Search for subtitle files. Right now only VobSub is supported
        """
        base = os.path.splitext(filename)[0]
        if os.path.isfile(base + '.idx') and (os.path.isfile(base + '.sub') or os.path.isfile(base + '.rar')):
            file = open(base + '.idx')
            if file.readline().find('VobSub index file') > 0:
                for line in file.readlines():
                    if line.find('id') == 0:
                        sub = core.Subtitle()
                        sub.language = line[4:6]
                        sub.trackno = base + '.idx'
                        self.subtitles.append(sub)

            file.close()

    def _parseAVIH(self, t):
        retval = {}
        v = struct.unpack('<IIIIIIIIIIIIII', t[0:56])
        retval['dwMicroSecPerFrame'], retval['dwMaxBytesPerSec'], retval['dwPaddingGranularity'], retval['dwFlags'], retval['dwTotalFrames'], retval['dwInitialFrames'], retval['dwStreams'], retval['dwSuggestedBufferSize'], retval['dwWidth'], retval['dwHeight'], retval['dwScale'], retval['dwRate'], retval['dwStart'], retval['dwLength'] = v
        if retval['dwMicroSecPerFrame'] == 0:
            log.warning('ERROR: Corrupt AVI')
            raise core.ParseError()
        return retval

    def _parseSTRH(self, t):
        retval = {}
        retval['fccType'] = t[0:4]
        log.debug('_parseSTRH(%s) : %d bytes' % (retval['fccType'], len(t)))
        if retval['fccType'] != 'auds':
            retval['fccHandler'] = t[4:8]
            v = struct.unpack('<IHHIIIIIIIII', t[8:52])
            retval['dwFlags'], retval['wPriority'], retval['wLanguage'], retval['dwInitialFrames'], retval['dwScale'], retval['dwRate'], retval['dwStart'], retval['dwLength'], retval['dwSuggestedBufferSize'], retval['dwQuality'], retval['dwSampleSize'], retval['rcFrame'] = v
        else:
            try:
                v = struct.unpack('<IHHIIIIIIIII', t[8:52])
                retval['dwFlags'], retval['wPriority'], retval['wLanguage'], retval['dwInitialFrames'], retval['dwScale'], retval['dwRate'], retval['dwStart'], retval['dwLength'], retval['dwSuggestedBufferSize'], retval['dwQuality'], retval['dwSampleSize'], retval['rcFrame'] = v
                self.delay = float(retval['dwStart']) / (float(retval['dwRate']) / retval['dwScale'])
            except (KeyError, IndexError, ValueError, ZeroDivisionError):
                pass

        return retval

    def _parseSTRF(self, t, strh):
        fccType = strh['fccType']
        retval = {}
        if fccType == 'auds':
            retval['wFormatTag'], retval['nChannels'], retval['nSamplesPerSec'], retval['nAvgBytesPerSec'], retval['nBlockAlign'], retval['nBitsPerSample'] = struct.unpack('<HHHHHH', t[0:12])
            ai = core.AudioStream()
            ai.samplerate = retval['nSamplesPerSec']
            ai.channels = retval['nChannels']
            ai.codec = retval['wFormatTag']
            self.audio.append(ai)
        elif fccType == 'vids':
            v = struct.unpack('<IIIHH', t[0:16])
            retval['biSize'], retval['biWidth'], retval['biHeight'], retval['biPlanes'], retval['biBitCount'] = v
            v = struct.unpack('IIIII', t[20:40])
            retval['biSizeImage'], retval['biXPelsPerMeter'], retval['biYPelsPerMeter'], retval['biClrUsed'], retval['biClrImportant'] = v
            vi = core.VideoStream()
            vi.codec = t[16:20]
            vi.width = retval['biWidth']
            vi.height = retval['biHeight']
            vi.fps = float(strh['dwRate']) / strh['dwScale']
            vi.length = strh['dwLength'] / vi.fps
            self.video.append(vi)
        return retval

    def _parseSTRL(self, t):
        retval = {}
        size = len(t)
        i = 0
        while i < len(t) - 8:
            key = t[i:i + 4]
            sz = struct.unpack('<I', t[i + 4:i + 8])[0]
            i += 8
            value = t[i:]
            if key == 'strh':
                retval[key] = self._parseSTRH(value)
            elif key == 'strf':
                retval[key] = self._parseSTRF(value, retval['strh'])
            else:
                log.debug("_parseSTRL: unsupported stream tag '%s'", key)
            i += sz

        return (retval, i)

    def _parseODML(self, t):
        retval = {}
        size = len(t)
        i = 0
        key = t[i:i + 4]
        sz = struct.unpack('<I', t[i + 4:i + 8])[0]
        i += 8
        value = t[i:]
        if key != 'dmlh':
            log.debug('_parseODML: Error')
        i += sz - 8
        return (retval, i)

    def _parseVPRP(self, t):
        retval = {}
        v = struct.unpack('<IIIIIIIIII', t[:40])
        retval['VideoFormat'], retval['VideoStandard'], retval['RefreshRate'], retval['HTotalIn'], retval['VTotalIn'], retval['FrameAspectRatio'], retval['wPixel'], retval['hPixel'] = v[1:-1]
        r = retval['FrameAspectRatio']
        r = float(r >> 16) / (r & 65535)
        retval['FrameAspectRatio'] = r
        if self.video:
            map(lambda v: setattr(v, 'aspect', r), self.video)
        return (
         retval, v[0])

    def _parseLISTmovi(self, size, file):
        """
        Digs into movi list, looking for a Video Object Layer header in an
        mpeg4 stream in order to determine aspect ratio.
        """
        i = 0
        n_dc = 0
        done = False
        while i < min(5242880, size - 8) and n_dc < 5:
            data = file.read(8)
            if ord(data[0]) == 0:
                data = data[1:] + file.read(1)
                i += 1
            key, sz = struct.unpack('<4sI', data)
            if key[2:] != 'dc' or sz > 512000:
                file.seek(sz, 1)
                i += 8 + sz
                continue
            n_dc += 1
            data = file.read(sz)
            pos = 0
            startcode = 255

            def bits(v, o, n):
                return (v & 2 ** n - 1 << 64 - n - o) >> 64 - n - o

            while pos < sz:
                startcode = (startcode << 8 | ord(data[pos])) & 4294967295
                pos += 1
                if startcode & 4294967040 != 256:
                    continue
                if startcode >= 288 and startcode <= 303:
                    v = struct.unpack('>Q', data[pos:pos + 8])[0]
                    offset = 10
                    if bits(v, 9, 1):
                        offset += 7
                    ar_info = bits(v, offset, 4)
                    if ar_info == 15:
                        num = bits(v, offset + 4, 8)
                        den = bits(v, offset + 12, 8)
                    else:
                        num, den = PIXEL_ASPECT.get(ar_info, (0, 0))
                    if 0 not in (num, den):
                        width, height = self.video[(-1)].width, self.video[(-1)].height
                        self.video[(-1)].aspect = num / float(den) * width / height
                    done = True
                    break
                startcode = 255

            i += 8 + len(data)
            if done:
                break

        if i < size:
            file.seek(size - i, 1)

    def _parseLIST(self, t):
        retval = {}
        i = 0
        size = len(t)
        while i < size - 8:
            if ord(t[i]) == 0:
                i += 1
            key = t[i:i + 4]
            sz = 0
            if key == 'LIST':
                sz = struct.unpack('<I', t[i + 4:i + 8])[0]
                i += 8
                key = 'LIST:' + t[i:i + 4]
                value = self._parseLIST(t[i:i + sz])
                if key == 'strl':
                    for k in value.keys():
                        retval[k] = value[k]

                else:
                    retval[key] = value
                i += sz
            elif key == 'avih':
                sz = struct.unpack('<I', t[i + 4:i + 8])[0]
                i += 8
                value = self._parseAVIH(t[i:i + sz])
                i += sz
                retval[key] = value
            elif key == 'strl':
                i += 4
                value, sz = self._parseSTRL(t[i:])
                key = value['strh']['fccType']
                i += sz
                retval[key] = value
            elif key == 'odml':
                i += 4
                value, sz = self._parseODML(t[i:])
                i += sz
            elif key == 'vprp':
                i += 4
                value, sz = self._parseVPRP(t[i:])
                retval[key] = value
                i += sz
            elif key == 'JUNK':
                sz = struct.unpack('<I', t[i + 4:i + 8])[0]
                i += sz + 8
            else:
                sz = struct.unpack('<I', t[i + 4:i + 8])[0]
                i += 8
                if key not in AVIINFO.keys() and key != 'IDIT':
                    log.debug('Unknown Key: %s, len: %d' % (key, sz))
                value = t[i:i + sz]
                if key == 'ISFT':
                    if value.find('\x00') > 0:
                        value = value[:value.find('\x00')]
                    value = value.replace('\x00', '').lstrip().rstrip()
                value = value.replace('\x00', '').lstrip().rstrip()
                if value:
                    retval[key] = value
                    if key in ('IDIT', 'ICRD'):
                        specs = ('%a %b %d %H:%M:%S %Y', '%Y/%m/%d/ %H:%M', '%B %d, %Y')
                        for tmspec in specs:
                            try:
                                tm = time.strptime(value, tmspec)
                                self.timestamp = int(time.mktime(tm))
                                break
                            except ValueError:
                                pass

                        else:
                            log.debug('no support for time format %s', value)

                i += sz

        return retval

    def _parseRIFFChunk(self, file):
        h = file.read(8)
        if len(h) < 8:
            return False
        name = h[:4]
        size = struct.unpack('<I', h[4:8])[0]
        if name == 'LIST':
            pos = file.tell() - 8
            key = file.read(4)
            if key == 'movi' and self.video and not self.video[(-1)].aspect and self.video[(-1)].width and self.video[(-1)].height and self.video[(-1)].format in ('DIVX',
                                                                                                                                                                   'XVID',
                                                                                                                                                                   'FMP4'):
                self._parseLISTmovi(size - 4, file)
                return True
            if size > 80000:
                log.debug('RIFF LIST "%s" too long to parse: %s bytes' % (key, size))
                t = file.seek(size - 4, 1)
                return True
            if size < 5:
                log.debug('RIFF LIST "%s" too short: %s bytes' % (key, size))
                return True
            t = file.read(size - 4)
            log.debug('parse RIFF LIST "%s": %d bytes' % (key, size))
            value = self._parseLIST(t)
            self.header[key] = value
            if key == 'INFO':
                self.infoStart = pos
                self._appendtable('AVIINFO', value)
            elif key == 'MID ':
                self._appendtable('AVIMID', value)
            elif key in ('hdrl', ):
                pass
            else:
                log.debug('Skipping table info %s' % key)
        elif name == 'JUNK':
            self.junkStart = file.tell() - 8
            self.junkSize = size
            file.seek(size, 1)
        elif name == 'idx1':
            self.has_idx = True
            log.debug('idx1: %s bytes' % size)
            t = file.seek(size, 1)
        else:
            if name == 'RIFF':
                log.debug('New RIFF chunk, extended avi [%i]' % size)
                type = file.read(4)
                if type != 'AVIX':
                    log.debug('Second RIFF chunk is %s, not AVIX, skipping', type)
                    file.seek(size - 4, 1)
                return False
            if name == 'fmt ' and size <= 50:
                self.media = core.MEDIA_AUDIO
                data = file.read(size)
                fmt = struct.unpack('<HHLLHH', data[:16])
                self._set('codec', hex(fmt[0]))
                self._set('samplerate', fmt[2])
                self._set('bitrate', fmt[3] / 125)
                self._set('byterate', fmt[3])
                self._set('fourcc', 'dummy')
            elif name == 'data':
                self._set('length', size / float(self.byterate))
                file.seek(size, 1)
            elif not name.strip(string.printable + string.whitespace):
                t = file.seek(size, 1)
                log.debug('Skipping %s [%i]' % (name, size))
            else:
                log.debug('Bad or broken avi')
                return False
        return True


Parser = Riff