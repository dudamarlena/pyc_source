# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/video/mp4.py
# Compiled at: 2010-09-04 10:26:27
__all__ = [
 'Parser']
import zlib, logging, StringIO, struct, core
log = logging.getLogger('metadata')
QTUDTA = {'nam': 'title', 
   'aut': 'artist', 
   'cpy': 'copyright'}
QTLANGUAGES = {0: 'en', 
   1: 'fr', 
   2: 'de', 
   3: 'it', 
   4: 'nl', 
   5: 'sv', 
   6: 'es', 
   7: 'da', 
   8: 'pt', 
   9: 'no', 
   10: 'he', 
   11: 'ja', 
   12: 'ar', 
   13: 'fi', 
   14: 'el', 
   15: 'is', 
   16: 'mt', 
   17: 'tr', 
   18: 'hr', 
   19: 'Traditional Chinese', 
   20: 'ur', 
   21: 'hi', 
   22: 'th', 
   23: 'ko', 
   24: 'lt', 
   25: 'pl', 
   26: 'hu', 
   27: 'et', 
   28: 'lv', 
   29: 'Lappish', 
   30: 'fo', 
   31: 'Farsi', 
   32: 'ru', 
   33: 'Simplified Chinese', 
   34: 'Flemish', 
   35: 'ga', 
   36: 'sq', 
   37: 'ro', 
   38: 'cs', 
   39: 'sk', 
   40: 'sl', 
   41: 'yi', 
   42: 'sr', 
   43: 'mk', 
   44: 'bg', 
   45: 'uk', 
   46: 'be', 
   47: 'uz', 
   48: 'kk', 
   49: 'az', 
   50: 'AzerbaijanAr', 
   51: 'hy', 
   52: 'ka', 
   53: 'mo', 
   54: 'ky', 
   55: 'tg', 
   56: 'tk', 
   57: 'mn', 
   58: 'MongolianCyr', 
   59: 'ps', 
   60: 'ku', 
   61: 'ks', 
   62: 'sd', 
   63: 'bo', 
   64: 'ne', 
   65: 'sa', 
   66: 'mr', 
   67: 'bn', 
   68: 'as', 
   69: 'gu', 
   70: 'pa', 
   71: 'or', 
   72: 'ml', 
   73: 'kn', 
   74: 'ta', 
   75: 'te', 
   76: 'si', 
   77: 'my', 
   78: 'Khmer', 
   79: 'lo', 
   80: 'vi', 
   81: 'id', 
   82: 'tl', 
   83: 'MalayRoman', 
   84: 'MalayArabic', 
   85: 'am', 
   86: 'ti', 
   87: 'om', 
   88: 'so', 
   89: 'sw', 
   90: 'Ruanda', 
   91: 'Rundi', 
   92: 'Chewa', 
   93: 'mg', 
   94: 'eo', 
   128: 'cy', 
   129: 'eu', 
   130: 'ca', 
   131: 'la', 
   132: 'qu', 
   133: 'gn', 
   134: 'ay', 
   135: 'tt', 
   136: 'ug', 
   137: 'Dzongkha', 
   138: 'JavaneseRom'}

class MPEG4(core.AVContainer):
    """
    Parser for the MP4 container format. This format is mostly
    identical to Apple Quicktime and 3GP files. It maps to mp4, mov,
    qt and some other extensions.
    """
    table_mapping = {'QTUDTA': QTUDTA}

    def __init__(self, file):
        core.AVContainer.__init__(self)
        self._references = []
        self.mime = 'video/quicktime'
        self.type = 'Quicktime Video'
        h = file.read(8)
        try:
            size, type = struct.unpack('>I4s', h)
        except struct.error:
            raise core.ParseError()

        if type == 'ftyp':
            if size >= 12:
                if file.read(4) != 'qt  ':
                    self.mime = 'video/mp4'
                    self.type = 'MPEG-4 Video'
                size -= 4
            file.seek(size - 8, 1)
            h = file.read(8)
            size, type = struct.unpack('>I4s', h)
        while type in ('mdat', 'skip'):
            file.seek(size - 8, 1)
            h = file.read(8)
            size, type = struct.unpack('>I4s', h)

        if type not in ('moov', 'wide', 'free'):
            log.debug('invalid header: %r' % type)
            raise core.ParseError()
        if size == 1:
            size = struct.unpack('>Q', file.read(8))
        file.seek(-8, 1)
        while self._readatom(file):
            pass

        if self._references:
            self._set('references', self._references)

    def _readatom(self, file):
        s = file.read(8)
        if len(s) < 8:
            return 0
        else:
            atomsize, atomtype = struct.unpack('>I4s', s)
            if not str(atomtype).decode('latin1').isalnum():
                return 0
            log.debug('%s [%X]' % (atomtype, atomsize))
            if atomtype == 'udta':
                pos = 0
                tabl = {}
                i18ntabl = {}
                atomdata = file.read(atomsize - 8)
                while pos < atomsize - 12:
                    datasize, datatype = struct.unpack('>I4s', atomdata[pos:pos + 8])
                    if ord(datatype[0]) == 169:
                        mypos = 8 + pos
                        while mypos + 4 < datasize + pos:
                            tlen, lang = struct.unpack('>HH', atomdata[mypos:mypos + 4])
                            i18ntabl[lang] = i18ntabl.get(lang, {})
                            l = atomdata[mypos + 4:mypos + tlen + 4]
                            i18ntabl[lang][datatype[1:]] = l
                            mypos += tlen + 4

                    elif datatype == 'WLOC':
                        pass
                    elif ord(atomdata[pos + 8:pos + datasize][0]) > 1:
                        tabl[datatype] = atomdata[pos + 8:pos + datasize]
                    pos += datasize

                if len(i18ntabl.keys()) > 0:
                    for k in i18ntabl.keys():
                        if QTLANGUAGES.has_key(k) and QTLANGUAGES[k] == 'en':
                            self._appendtable('QTUDTA', i18ntabl[k])
                            self._appendtable('QTUDTA', tabl)

                else:
                    log.debug('NO i18')
                    self._appendtable('QTUDTA', tabl)
            elif atomtype == 'trak':
                atomdata = file.read(atomsize - 8)
                pos = 0
                trackinfo = {}
                tracktype = None
                while pos < atomsize - 8:
                    datasize, datatype = struct.unpack('>I4s', atomdata[pos:pos + 8])
                    if datatype == 'tkhd':
                        tkhd = struct.unpack('>6I8x4H36xII', atomdata[pos + 8:pos + datasize])
                        trackinfo['width'] = tkhd[10] >> 16
                        trackinfo['height'] = tkhd[11] >> 16
                        trackinfo['id'] = tkhd[3]
                        try:
                            self.timestamp = int(tkhd[1]) - 2082844800
                        except Exception as e:
                            log.exception('There was trouble extracting timestamp')

                    elif datatype == 'mdia':
                        pos += 8
                        datasize -= 8
                        log.debug('--> mdia information')
                        while datasize:
                            mdia = struct.unpack('>I4s', atomdata[pos:pos + 8])
                            if mdia[1] == 'mdhd':
                                ver = ord(atomdata[(pos + 8)])
                                if ver == 0:
                                    mdhd = struct.unpack('>IIIIIhh', atomdata[pos + 8:pos + 8 + 24])
                                elif ver == 1:
                                    mdhd = struct.unpack('>IQQIQhh', atomdata[pos + 8:pos + 8 + 36])
                                else:
                                    mdhd = None
                                if mdhd:
                                    trackinfo['length'] = mdhd[4] / mdhd[3]
                                    if mdhd[5] in QTLANGUAGES:
                                        trackinfo['language'] = QTLANGUAGES[mdhd[5]]
                                    self.length = max(self.length, mdhd[4] / mdhd[3])
                            elif mdia[1] == 'minf':
                                pos -= mdia[0] - 8
                                datasize += mdia[0] - 8
                            elif mdia[1] == 'stbl':
                                pos -= mdia[0] - 8
                                datasize += mdia[0] - 8
                            elif mdia[1] == 'hdlr':
                                hdlr = struct.unpack('>I4s4s', atomdata[pos + 8:pos + 8 + 12])
                                if hdlr[1] == 'mhlr':
                                    if hdlr[2] == 'vide':
                                        tracktype = 'video'
                                    if hdlr[2] == 'soun':
                                        tracktype = 'audio'
                            elif mdia[1] == 'stsd':
                                stsd = struct.unpack('>2I', atomdata[pos + 8:pos + 8 + 8])
                                if stsd[1] > 0:
                                    codec = atomdata[pos + 16:pos + 16 + 8]
                                    codec = struct.unpack('>I4s', codec)
                                    trackinfo['codec'] = codec[1]
                                    if codec[1] == 'jpeg':
                                        tracktype = 'image'
                            elif mdia[1] == 'dinf':
                                dref = struct.unpack('>I4s', atomdata[pos + 8:pos + 8 + 8])
                                log.debug('  --> %s, %s (useless)' % mdia)
                                if dref[1] == 'dref':
                                    num = struct.unpack('>I', atomdata[pos + 20:pos + 20 + 4])[0]
                                    rpos = pos + 20 + 4
                                    for ref in range(num):
                                        ref = struct.unpack('>I3s', atomdata[rpos:rpos + 7])
                                        data = atomdata[rpos + 7:rpos + ref[0]]
                                        rpos += ref[0]

                            elif mdia[1].startswith('st'):
                                log.debug('  --> %s, %s (sample)' % mdia)
                            elif mdia[1] in ('vmhd', ) and not tracktype:
                                tracktype = 'video'
                            elif mdia[1] in ('vmhd', 'smhd') and not tracktype:
                                tracktype = 'audio'
                            else:
                                log.debug('  --> %s, %s (unknown)' % mdia)
                            pos += mdia[0]
                            datasize -= mdia[0]

                    elif datatype == 'udta':
                        log.debug(struct.unpack('>I4s', atomdata[:8]))
                    elif datatype == 'edts':
                        log.debug('--> %s [%d] (edit list)' % (
                         datatype, datasize))
                    else:
                        log.debug('--> %s [%d] (unknown)' % (
                         datatype, datasize))
                    pos += datasize

                info = None
                if tracktype == 'video':
                    info = core.VideoStream()
                    self.video.append(info)
                if tracktype == 'audio':
                    info = core.AudioStream()
                    self.audio.append(info)
                if info:
                    for key, value in trackinfo.items():
                        setattr(info, key, value)

            elif atomtype == 'mvhd':
                mvhd = struct.unpack('>6I2h', file.read(28))
                self.length = max(self.length, mvhd[4] / mvhd[3])
                self.volume = mvhd[6]
                file.seek(atomsize - 8 - 28, 1)
            elif atomtype == 'cmov':
                datasize, atomtype = struct.unpack('>I4s', file.read(8))
                if not atomtype == 'dcom':
                    return atomsize
                method = struct.unpack('>4s', file.read(datasize - 8))[0]
                datasize, atomtype = struct.unpack('>I4s', file.read(8))
                if not atomtype == 'cmvd':
                    return atomsize
                if method == 'zlib':
                    data = file.read(datasize - 8)
                    try:
                        decompressed = zlib.decompress(data)
                    except Exception as e:
                        try:
                            decompressed = zlib.decompress(data[4:])
                        except Exception as e:
                            log.exception('There was a proble decompressiong atom')
                            return atomsize

                    decompressedIO = StringIO.StringIO(decompressed)
                    while self._readatom(decompressedIO):
                        pass

                else:
                    log.info('unknown compression %s' % method)
                    file.seek(datasize - 8, 1)
            elif atomtype == 'moov':
                while self._readatom(file):
                    pass

            elif atomtype == 'mdat':
                pos = file.tell() + atomsize - 8
                log.info('parsing mdat')
                while self._readatom(file):
                    pass

                log.info('end of mdat')
                file.seek(pos, 0)
            elif atomtype == 'rmra':
                while self._readatom(file):
                    pass

            elif atomtype == 'rmda':
                atomdata = file.read(atomsize - 8)
                pos = 0
                url = ''
                quality = 0
                datarate = 0
                while pos < atomsize - 8:
                    datasize, datatype = struct.unpack('>I4s', atomdata[pos:pos + 8])
                    if datatype == 'rdrf':
                        rflags, rtype, rlen = struct.unpack('>I4sI', atomdata[pos + 8:pos + 20])
                        if rtype == 'url ':
                            url = atomdata[pos + 20:pos + 20 + rlen]
                            if url.find('\x00') > 0:
                                url = url[:url.find('\x00')]
                    elif datatype == 'rmqu':
                        quality = struct.unpack('>I', atomdata[pos + 8:pos + 12])[0]
                    elif datatype == 'rmdr':
                        datarate = struct.unpack('>I', atomdata[pos + 12:pos + 16])[0]
                    pos += datasize

                if url:
                    self._references.append((url, quality, datarate))
            else:
                if atomtype not in ('wide', 'free'):
                    log.info('unhandled base atom %s' % atomtype)
                try:
                    file.seek(atomsize - 8, 1)
                except IOError:
                    return 0

            return atomsize


Parser = MPEG4