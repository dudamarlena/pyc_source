# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/audio/id3.py
# Compiled at: 2009-09-07 17:44:28
"""
ID3 metadata parser, supported versions: 1.O, 2.2, 2.3 and 2.4

Informations: http://www.id3.org/

Author: Victor Stinner
"""
from hachoir_core.field import FieldSet, MatchError, ParserError, Enum, UInt8, UInt24, UInt32, CString, String, RawBytes, Bit, Bits, NullBytes, NullBits
from hachoir_core.text_handler import textHandler
from hachoir_core.tools import humanDuration
from hachoir_core.endian import NETWORK_ENDIAN

class ID3v1(FieldSet):
    __module__ = __name__
    static_size = 128 * 8
    GENRE_NAME = {0: 'Blues', 1: 'Classic Rock', 2: 'Country', 3: 'Dance', 4: 'Disco', 5: 'Funk', 6: 'Grunge', 7: 'Hip-Hop', 8: 'Jazz', 9: 'Metal', 10: 'New Age', 11: 'Oldies', 12: 'Other', 13: 'Pop', 14: 'R&B', 15: 'Rap', 16: 'Reggae', 17: 'Rock', 18: 'Techno', 19: 'Industrial', 20: 'Alternative', 21: 'Ska', 22: 'Death Metal', 23: 'Pranks', 24: 'Soundtrack', 25: 'Euro-Techno', 26: 'Ambient', 27: 'Trip-Hop', 28: 'Vocal', 29: 'Jazz+Funk', 30: 'Fusion', 31: 'Trance', 32: 'Classical', 33: 'Instrumental', 34: 'Acid', 35: 'House', 36: 'Game', 37: 'Sound Clip', 38: 'Gospel', 39: 'Noise', 40: 'AlternRock', 41: 'Bass', 42: 'Soul', 43: 'Punk', 44: 'Space', 45: 'Meditative', 46: 'Instrumental Pop', 47: 'Instrumental Rock', 48: 'Ethnic', 49: 'Gothic', 50: 'Darkwave', 51: 'Techno-Industrial', 52: 'Electronic', 53: 'Pop-Folk', 54: 'Eurodance', 55: 'Dream', 56: 'Southern Rock', 57: 'Comedy', 58: 'Cult', 59: 'Gangsta', 60: 'Top 40', 61: 'Christian Rap', 62: 'Pop/Funk', 63: 'Jungle', 64: 'Native American', 65: 'Cabaret', 66: 'New Wave', 67: 'Psychadelic', 68: 'Rave', 69: 'Showtunes', 70: 'Trailer', 71: 'Lo-Fi', 72: 'Tribal', 73: 'Acid Punk', 74: 'Acid Jazz', 75: 'Polka', 76: 'Retro', 77: 'Musical', 78: 'Rock & Roll', 79: 'Hard Rock', 80: 'Folk', 81: 'Folk-Rock', 82: 'National Folk', 83: 'Swing', 84: 'Fast Fusion', 85: 'Bebob', 86: 'Latin', 87: 'Revival', 88: 'Celtic', 89: 'Bluegrass', 90: 'Avantgarde', 91: 'Gothic Rock', 92: 'Progressive Rock', 93: 'Psychedelic Rock', 94: 'Symphonic Rock', 95: 'Slow Rock', 96: 'Big Band', 97: 'Chorus', 98: 'Easy Listening', 99: 'Acoustic', 100: 'Humour', 101: 'Speech', 102: 'Chanson', 103: 'Opera', 104: 'Chamber Music', 105: 'Sonata', 106: 'Symphony', 107: 'Booty Bass', 108: 'Primus', 109: 'Porn Groove', 110: 'Satire', 111: 'Slow Jam', 112: 'Club', 113: 'Tango', 114: 'Samba', 115: 'Folklore', 116: 'Ballad', 117: 'Power Ballad', 118: 'Rhythmic Soul', 119: 'Freestyle', 120: 'Duet', 121: 'Punk Rock', 122: 'Drum Solo', 123: 'A capella', 124: 'Euro-House', 125: 'Dance Hall', 126: 'Goa', 127: 'Drum & Bass', 128: 'Club-House', 129: 'Hardcore', 130: 'Terror', 131: 'Indie', 132: 'Britpop', 133: 'Negerpunk', 134: 'Polsk Punk', 135: 'Beat', 136: 'Christian Gangsta Rap', 137: 'Heavy Metal', 138: 'Black Metal', 139: 'Crossover', 140: 'Contemporary Christian', 141: 'Christian Rock ', 142: 'Merengue', 143: 'Salsa', 144: 'Trash Metal', 145: 'Anime', 146: 'JPop', 147: 'Synthpop'}

    def createFields(self):
        yield String(self, 'signature', 3, 'IDv1 signature ("TAG")', charset='ASCII')
        if self['signature'].value != 'TAG':
            raise MatchError("Stream doesn't look like ID3v1 (wrong signature)!")
        yield String(self, 'song', 30, 'Song title', strip=' \x00', charset='ISO-8859-1')
        yield String(self, 'author', 30, 'Author', strip=' \x00', charset='ISO-8859-1')
        yield String(self, 'album', 30, 'Album title', strip=' \x00', charset='ISO-8859-1')
        yield String(self, 'year', 4, 'Year', strip=' \x00', charset='ISO-8859-1')
        version = self.getVersion()
        if version in ('v1.1', 'v1.1b'):
            if version == 'v1.1b':
                yield String(self, 'comment', 29, 'Comment', strip=' \x00', charset='ISO-8859-1')
                yield UInt8(self, 'track_nb', 'Track number')
            else:
                yield String(self, 'comment', 30, 'Comment', strip=' \x00', charset='ISO-8859-1')
            yield Enum(UInt8(self, 'genre', 'Genre'), self.GENRE_NAME)
        else:
            yield String(self, 'comment', 31, 'Comment', strip=' \x00', charset='ISO-8859-1')

    def getVersion(self):
        addr = self.absolute_address + 126 * 8
        bytes = self.stream.readBytes(addr, 2)
        if bytes[1] != ' ':
            if bytes[0] == 0:
                return 'v1.1'
            else:
                return 'v1.1b'
        else:
            return '1.0'

    def createDescription(self):
        version = self.getVersion()
        return 'ID3 %s: author=%s, song=%s' % (version, self['author'].value, self['song'].value)


def getCharset(field):
    try:
        key = field.value
        return ID3_StringCharset.charset_name[key]
    except KeyError:
        raise ParserError('ID3v2: Invalid charset (%s).' % key)


class ID3_String(FieldSet):
    __module__ = __name__
    STRIP = ' \x00'

    def createFields(self):
        yield String(self, 'text', self._size / 8, 'Text', charset='ISO-8859-1', strip=self.STRIP)


class ID3_StringCharset(ID3_String):
    __module__ = __name__
    STRIP = ' \x00'
    charset_desc = {0: 'ISO-8859-1', 1: 'UTF-16 with BOM', 2: 'UTF-16 (big endian)', 3: 'UTF-8'}
    charset_name = {0: 'ISO-8859-1', 1: 'UTF-16', 2: 'UTF-16-BE', 3: 'UTF-8'}

    def createFields(self):
        yield Enum(UInt8(self, 'charset'), self.charset_desc)
        size = (self.size - self.current_size) / 8
        if not size:
            return
        charset = getCharset(self['charset'])
        yield String(self, 'text', size, 'Text', charset=charset, strip=self.STRIP)


class ID3_GEOB(ID3_StringCharset):
    __module__ = __name__

    def createFields(self):
        yield Enum(UInt8(self, 'charset'), self.charset_desc)
        charset = getCharset(self['charset'])
        yield CString(self, 'mime', 'MIME type', charset=charset)
        yield CString(self, 'filename', 'File name', charset=charset)
        yield CString(self, 'description', 'Content description', charset=charset)
        size = (self.size - self.current_size) // 8
        if not size:
            return
        yield String(self, 'text', size, 'Text', charset=charset)


class ID3_Comment(ID3_StringCharset):
    __module__ = __name__

    def createFields(self):
        yield Enum(UInt8(self, 'charset'), self.charset_desc)
        yield String(self, 'lang', 3, 'Language', charset='ASCII')
        charset = getCharset(self['charset'])
        yield CString(self, 'title', 'Title', charset=charset, strip=self.STRIP)
        size = (self.size - self.current_size) // 8
        if not size:
            return
        yield String(self, 'text', size, 'Text', charset=charset, strip=self.STRIP)


class ID3_StringTitle(ID3_StringCharset):
    __module__ = __name__

    def createFields(self):
        yield Enum(UInt8(self, 'charset'), self.charset_desc)
        if self.current_size == self.size:
            return
        charset = getCharset(self['charset'])
        yield CString(self, 'title', 'Title', charset=charset, strip=self.STRIP)
        size = (self.size - self.current_size) / 8
        if not size:
            return
        yield String(self, 'text', size, 'Text', charset=charset, strip=self.STRIP)


class ID3_Private(FieldSet):
    __module__ = __name__

    def createFields(self):
        size = self._size / 8
        if self.stream.readBytes(self.absolute_address, 9) == 'PeakValue':
            yield String(self, 'text', 9, 'Text')
            size -= 9
        yield String(self, 'content', size, 'Content')


class ID3_TrackLength(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield NullBytes(self, 'zero', 1)
        yield textHandler(String(self, 'length', self._size / 8 - 1, 'Length in ms', charset='ASCII'), self.computeLength)

    def computeLength(self, field):
        try:
            ms = int(field.value)
            return humanDuration(ms)
        except:
            return field.value


class ID3_Picture23(FieldSet):
    __module__ = __name__
    pict_type_name = {0: 'Other', 1: "32x32 pixels 'file icon' (PNG only)", 2: 'Other file icon', 3: 'Cover (front)', 4: 'Cover (back)', 5: 'Leaflet page', 6: 'Media (e.g. lable side of CD)', 7: 'Lead artist/lead performer/soloist', 8: 'Artist/performer', 9: 'Conductor', 10: 'Band/Orchestra', 11: 'Composer', 12: 'Lyricist/text writer', 13: 'Recording Location', 14: 'During recording', 15: 'During performance', 16: 'Movie/video screen capture', 17: 'A bright coloured fish', 18: 'Illustration', 19: 'Band/artist logotype', 20: 'Publisher/Studio logotype'}

    def createFields(self):
        yield Enum(UInt8(self, 'charset'), ID3_StringCharset.charset_desc)
        charset = getCharset(self['charset'])
        yield String(self, 'img_fmt', 3, charset='ASCII')
        yield Enum(UInt8(self, 'pict_type'), self.pict_type_name)
        yield CString(self, 'text', 'Text', charset=charset, strip=' \x00')
        size = (self._size - self._current_size) / 8
        if size:
            yield RawBytes(self, 'img_data', size)


class ID3_Picture24(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield Enum(UInt8(self, 'charset'), ID3_StringCharset.charset_desc)
        charset = getCharset(self['charset'])
        yield CString(self, 'mime', 'MIME type', charset=charset)
        yield Enum(UInt8(self, 'pict_type'), ID3_Picture23.pict_type_name)
        yield CString(self, 'description', charset=charset)
        size = (self._size - self._current_size) / 8
        if size:
            yield RawBytes(self, 'img_data', size)


class ID3_Chunk(FieldSet):
    __module__ = __name__
    endian = NETWORK_ENDIAN
    tag22_name = {'TT2': 'Track title', 'TP1': 'Artist', 'TRK': 'Track number', 'COM': 'Comment', 'TCM': 'Composer', 'TAL': 'Album', 'TYE': 'Year', 'TEN': 'Encoder', 'TCO': 'Content type', 'PIC': 'Picture'}
    tag23_name = {'COMM': 'Comment', 'GEOB': 'Encapsulated object', 'PRIV': 'Private', 'TPE1': 'Artist', 'TCOP': 'Copyright', 'TALB': 'Album', 'TENC': 'Encoder', 'TYER': 'Year', 'TSSE': 'Encoder settings', 'TCOM': 'Composer', 'TRCK': 'Track number', 'PCNT': 'Play counter', 'TCON': 'Content type', 'TLEN': 'Track length', 'TIT2': 'Track title', 'WXXX': 'User defined URL'}
    handler = {'COMM': ID3_Comment, 'COM': ID3_Comment, 'GEOB': ID3_GEOB, 'PIC': ID3_Picture23, 'APIC': ID3_Picture24, 'PRIV': ID3_Private, 'TXXX': ID3_StringTitle, 'WOAR': ID3_String, 'WXXX': ID3_StringTitle}

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        if 3 <= self['../ver_major'].value:
            self._size = (10 + self['size'].value) * 8
        else:
            self._size = (self['size'].value + 6) * 8

    def createFields(self):
        if 3 <= self['../ver_major'].value:
            yield Enum(String(self, 'tag', 4, 'Tag', charset='ASCII', strip='\x00'), ID3_Chunk.tag23_name)
            if 4 <= self['../ver_major'].value:
                yield ID3_Size(self, 'size')
            else:
                yield UInt32(self, 'size')
            yield Bit(self, 'tag_alter', 'Tag alter preservation')
            yield Bit(self, 'file_alter', 'Tag alter preservation')
            yield Bit(self, 'rd_only', 'Read only?')
            yield NullBits(self, 'padding[]', 5)
            yield Bit(self, 'compressed', 'Frame is compressed?')
            yield Bit(self, 'encrypted', 'Frame is encrypted?')
            yield Bit(self, 'group', 'Grouping identity')
            yield NullBits(self, 'padding[]', 5)
            size = self['size'].value
            is_compressed = self['compressed'].value
        else:
            yield Enum(String(self, 'tag', 3, 'Tag', charset='ASCII', strip='\x00'), ID3_Chunk.tag22_name)
            yield UInt24(self, 'size')
            size = self['size'].value - self.current_size / 8 + 6
            is_compressed = False
        if size:
            cls = None
            if not is_compressed:
                tag = self['tag'].value
                if tag in ID3_Chunk.handler:
                    cls = ID3_Chunk.handler[tag]
                elif tag[0] == 'T':
                    cls = ID3_StringCharset
            if cls:
                yield cls(self, 'content', 'Content', size=size * 8)
            else:
                yield RawBytes(self, 'content', size, 'Raw data content')
        return

    def createDescription(self):
        if self['size'].value != 0:
            return 'ID3 Chunk: %s' % self['tag'].display
        else:
            return 'ID3 Chunk: (terminator)'


class ID3_Size(Bits):
    __module__ = __name__
    static_size = 32

    def __init__(self, parent, name, description=None):
        Bits.__init__(self, parent, name, 32, description)

    def createValue(self):
        data = self.parent.stream.readBytes(self.absolute_address, 4)
        return reduce(lambda x, y: x * 128 + y, (ord(item) for item in data))


class ID3v2(FieldSet):
    __module__ = __name__
    endian = NETWORK_ENDIAN
    VALID_MAJOR_VERSIONS = (2, 3, 4)

    def __init__(self, parent, name, size=None):
        FieldSet.__init__(self, parent, name, size=size)
        if not self._size:
            self._size = (self['size'].value + 10) * 8

    def createDescription(self):
        return 'ID3 v2.%s.%s' % (self['ver_major'].value, self['ver_minor'].value)

    def createFields(self):
        yield String(self, 'header', 3, 'Header (ID3)', charset='ASCII')
        yield UInt8(self, 'ver_major', 'Version (major)')
        yield UInt8(self, 'ver_minor', 'Version (minor)')
        if self['header'].value != 'ID3':
            raise MatchError('Signature error, should be "ID3".')
        if self['ver_major'].value not in self.VALID_MAJOR_VERSIONS or self['ver_minor'].value != 0:
            raise MatchError('Unknown ID3 metadata version (2.%u.%u)' % (self['ver_major'].value, self['ver_minor'].value))
        yield Bit(self, 'unsync', 'Unsynchronisation is used?')
        yield Bit(self, 'ext', 'Extended header is used?')
        yield Bit(self, 'exp', 'Experimental indicator')
        yield NullBits(self, 'padding[]', 5)
        yield ID3_Size(self, 'size')
        while self.current_size < self._size:
            field = ID3_Chunk(self, 'field[]')
            yield field
            if field['size'].value == 0:
                break

        padding = self.seekBit(self._size)
        if padding:
            yield padding