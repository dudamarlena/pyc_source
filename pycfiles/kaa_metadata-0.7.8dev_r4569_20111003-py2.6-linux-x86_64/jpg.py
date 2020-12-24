# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/image/jpg.py
# Compiled at: 2008-10-26 20:23:09
__all__ = [
 'Parser']
import struct, time, logging, cStringIO, core, EXIF, IPTC
log = logging.getLogger('metadata')
SOF = {192: 'Baseline', 193: 'Extended sequential', 
   194: 'Progressive', 
   195: 'Lossless', 
   197: 'Differential sequential', 
   198: 'Differential progressive', 
   199: 'Differential lossless', 
   201: 'Extended sequential, arithmetic coding', 
   202: 'Progressive, arithmetic coding', 
   203: 'Lossless, arithmetic coding', 
   205: 'Differential sequential, arithmetic coding', 
   206: 'Differential progressive, arithmetic coding', 
   207: 'Differential lossless, arithmetic coding'}
EXIFMap = {'Image Artist': 'artist', 
   'Image Model': 'hardware', 
   'Image Software': 'software'}

class JPG(core.Image):
    """
    JPEG parser supporting EXIf and IPTC tables. The important
    information is mapped to match the kaa.metadata key naming, the
    complete table can be accessed with self.tables.
    """
    table_mapping = {'EXIF': EXIFMap, 'IPTC': IPTC.mapping}

    def __init__(self, file):
        core.Image.__init__(self)
        self.mime = 'image/jpeg'
        self.type = 'jpeg image'
        if file.read(2) != b'\xff\xd8':
            raise core.ParseError()
        file.seek(-2, 2)
        if file.read(2) != b'\xff\xd9':
            log.info('Wrong encode found for jpeg')
        file.seek(2)
        app = file.read(4)
        self.meta = {}
        while len(app) == 4:
            ff, segtype, seglen = struct.unpack('>BBH', app)
            if ff != 255:
                break
            if segtype == 217:
                break
            elif SOF.has_key(segtype):
                data = file.read(seglen - 2)
                precision, self.height, self.width, num_comp = struct.unpack('>BHHB', data[:6])
            elif segtype == 225:
                data = file.read(seglen - 2)
                type = data[:data.find('\x00')]
                if type == 'Exif':
                    fakefile = cStringIO.StringIO()
                    fakefile.write(b'\xff\xd8')
                    fakefile.write(app)
                    fakefile.write(data)
                    fakefile.seek(0)
                    exif = EXIF.process_file(fakefile)
                    fakefile.close()
                    if exif:
                        self.thumbnail = exif.get('JPEGThumbnail', None)
                        if self.thumbnail:
                            self.thumbnail = str(self.thumbnail)
                        self._appendtable('EXIF', exif)
                        if 'Image Orientation' in exif:
                            orientation = str(exif['Image Orientation'])
                            if orientation.find('90 CW') > 0:
                                self.rotation = 90
                            elif orientation.find('90') > 0:
                                self.rotation = 270
                            elif orientation.find('180') > 0:
                                self.rotation = 180
                        t = exif.get('Image DateTimeOriginal')
                        if not t:
                            t = exif.get('EXIF DateTimeOriginal')
                        if not t:
                            t = exif.get('Image DateTime')
                        if t:
                            try:
                                t = time.strptime(str(t), '%Y:%m:%d %H:%M:%S')
                                self.timestamp = int(time.mktime(t))
                            except ValueError:
                                pass

                elif type == 'http://ns.adobe.com/xap/1.0/':
                    doc = data[data.find('\x00') + 1:]
            elif segtype == 237:
                iptc = IPTC.parseiptc(file.read(seglen - 2))
                if iptc:
                    self._appendtable('IPTC', iptc)
            elif segtype == 231:
                data = file.read(seglen - 2)
                if data.count('\n') == 1:
                    key, value = data.split('\n')
                    self.meta[key] = value
            elif segtype == 254:
                self.comment = file.read(seglen - 2)
                if self.comment.startswith('<?xml'):
                    log.error('xml comment parser not integrated')
                    self.comment = ''
            else:
                if segtype not in (196, 218, 219, 221):
                    log.info('SEGMENT: 0x%x%x, len=%d' % (ff, segtype, seglen))
                file.seek(seglen - 2, 1)
            app = file.read(4)

        if len(self.meta.keys()):
            self._appendtable('JPGMETA', self.meta)
        for key, value in self.meta.items():
            if key.startswith('Thumb:') or key == 'Software':
                self._set(key, value)

        return


Parser = JPG