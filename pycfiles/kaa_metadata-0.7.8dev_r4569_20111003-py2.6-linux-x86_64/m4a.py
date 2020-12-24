# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/m4a.py
# Compiled at: 2010-09-15 11:08:03
__all__ = [
 'Parser']
import logging, core
log = logging.getLogger('metadata')
import struct
FLAGS = CONTAINER, SKIPPER, TAGITEM, IGNORE = [ 2 ** _ for _ in xrange(4) ]
CALLBACK = TAGITEM
FLAGS.append(CALLBACK)
TAGTYPES = (
 (
  'ftyp', TAGITEM),
 ('mvhd', 0),
 (
  'moov', CONTAINER),
 ('mdat', 0),
 (
  'udta', CONTAINER),
 (
  'meta', CONTAINER | SKIPPER),
 (
  'ilst', CONTAINER),
 (
  b'\xa9ART', TAGITEM),
 (
  b'\xa9nam', TAGITEM),
 (
  b'\xa9too', TAGITEM),
 (
  b'\xa9alb', TAGITEM),
 (
  b'\xa9day', TAGITEM),
 (
  b'\xa9gen', TAGITEM),
 (
  b'\xa9wrt', TAGITEM),
 (
  b'\xa9cmt', TAGITEM),
 (
  'trkn', TAGITEM),
 (
  'trak', CONTAINER),
 (
  'mdia', CONTAINER),
 (
  'mdhd', TAGITEM),
 (
  'minf', CONTAINER),
 (
  'dinf', CONTAINER),
 (
  'stbl', CONTAINER))
flagged = {}
for flag in FLAGS:
    flagged[flag] = frozenset(_[0] for _ in TAGTYPES if _[1] & flag)

def _analyse(fp, offset0, offset1):
    """Walk the atom tree in a mp4 file"""
    offset = offset0
    while offset < offset1:
        fp.seek(offset)
        atomsize = struct.unpack('!i', fp.read(4))[0]
        atomtype = fp.read(4)
        if atomsize < 9:
            break
        if atomtype in flagged[CONTAINER]:
            data = ''
            for reply in _analyse(fp, offset + (atomtype in flagged[SKIPPER] and 12 or 8), offset + atomsize):
                yield reply

        else:
            fp.seek(offset + 8)
            if atomtype in flagged[TAGITEM]:
                data = fp.read(atomsize - 8)
            else:
                data = fp.read(min(atomsize - 8, 32))
        if atomtype not in flagged[IGNORE]:
            yield (atomtype, atomsize, data)
        offset += atomsize


def mp4_atoms(fp):
    fp.seek(0, 2)
    size = fp.tell()
    for atom in _analyse(fp, 0, size):
        yield atom


class M4ATags(dict):
    """An class reading .m4a tags"""
    convtag = {'ftyp': 'FileType', 
       'trkn': 'Track', 
       'length': 'Length', 
       'samplerate': 'SampleRate', 
       b'\xa9ART': 'Artist', 
       b'\xa9nam': 'Title', 
       b'\xa9alb': 'Album', 
       b'\xa9day': 'Year', 
       b'\xa9gen': 'Genre', 
       b'\xa9cmt': 'Comment', 
       b'\xa9wrt': 'Writer', 
       b'\xa9too': 'Tool'}

    def __init__(self, fp):
        super(dict, self).__init__()
        self['FileType'] = 'unknown'
        fp.seek(0, 0)
        try:
            size = struct.unpack('!i', fp.read(4))[0]
        except struct.error:
            return

        type = fp.read(4)
        if type == 'ftyp':
            for atomtype, atomsize, atomdata in mp4_atoms(fp):
                self.atom2tag(atomtype, atomdata)

    def atom2tag(self, atomtype, atomdata):
        """Insert items using descriptive key instead of atomtype"""
        if atomtype.find(b'\xa9', 0, 4) != -1:
            key = self.convtag[atomtype]
            self[key] = atomdata[16:].decode('utf-8')
        elif atomtype == 'mdhd':
            if ord(atomdata[0]) == 1:
                timescale = struct.unpack('!Q', atomdata[20:24])[0]
                duration = struct.unpack('!Q', atomdata[24:30])[0]
            else:
                timescale = struct.unpack('!i', atomdata[12:16])[0]
                duration = struct.unpack('!i', atomdata[16:20])[0]
            self[self.convtag['length']] = duration / timescale
            self[self.convtag['samplerate']] = timescale
        elif atomtype == 'trkn':
            self[self.convtag[atomtype]] = struct.unpack('!i', atomdata[16:20])[0]
        elif atomtype == 'ftyp':
            self[self.convtag[atomtype]] = atomdata[8:12].decode('utf-8')


class Mpeg4Audio(core.Music):

    def __init__(self, file):
        core.Music.__init__(self)
        tags = M4ATags(file)
        if tags.get('FileType') != 'M4A ':
            raise core.ParseError()
        self.valid = True
        self.mime = 'audio/mp4'
        self.filename = getattr(file, 'name', None)
        self.title = tags.get('Title')
        self.artist = tags.get('Artist')
        self.album = tags.get('Album')
        self.trackno = tags.get('Track')
        self.year = tags.get('Year')
        self.encoder = tags.get('Tool')
        self.length = tags.get('Length')
        self.samplerate = tags.get('SampleRate')
        return


Parser = Mpeg4Audio