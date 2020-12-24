# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/string_field.py
# Compiled at: 2009-09-07 17:44:28
"""
String field classes:
- String: Fixed length string (no prefix/no suffix) ;
- CString: String which ends with nul byte ("\x00") ;
- UnixLine: Unix line of text, string which ends with "
" ;
- PascalString8, PascalString16, PascalString32: String prefixed with
  length written in a 8, 16, 32-bit integer (use parent endian).

Constructor has optional arguments:
- strip: value can be a string or True ;
- charset: if set, convert string to unicode using this charset (in "replace"
  mode which replace all buggy characters with ".").

Note: For PascalStringXX, prefixed value is the number of bytes and not
      of characters!
"""
from hachoir_core.field import FieldError, Bytes
from hachoir_core.endian import LITTLE_ENDIAN, BIG_ENDIAN
from hachoir_core.tools import alignValue, makePrintable
from hachoir_core.i18n import guessBytesCharset, _
from hachoir_core import config
from codecs import BOM_UTF16_LE, BOM_UTF16_BE, BOM_UTF32_LE, BOM_UTF32_BE
FALLBACK_CHARSET = 'ISO-8859-1'

class GenericString(Bytes):
    """
    Generic string class.

    charset have to be in CHARSET_8BIT or in UTF_CHARSET.
    """
    __module__ = __name__
    VALID_FORMATS = ('C', 'UnixLine', 'fixed', 'Pascal8', 'Pascal16', 'Pascal32')
    CHARSET_8BIT = set(('ASCII', 'MacRoman', 'CP037', 'CP874', 'WINDOWS-1250', 'WINDOWS-1251',
                        'WINDOWS-1252', 'WINDOWS-1253', 'WINDOWS-1254', 'WINDOWS-1255',
                        'WINDOWS-1256', 'WINDOWS-1257', 'WINDOWS-1258', 'ISO-8859-1',
                        'ISO-8859-2', 'ISO-8859-3', 'ISO-8859-4', 'ISO-8859-5', 'ISO-8859-6',
                        'ISO-8859-7', 'ISO-8859-8', 'ISO-8859-9', 'ISO-8859-10',
                        'ISO-8859-11', 'ISO-8859-13', 'ISO-8859-14', 'ISO-8859-15',
                        'ISO-8859-16'))
    UTF_CHARSET = {'UTF-8': (8, None), 'UTF-16-LE': (16, LITTLE_ENDIAN), 'UTF-32LE': (32, LITTLE_ENDIAN), 'UTF-16-BE': (16, BIG_ENDIAN), 'UTF-32BE': (32, BIG_ENDIAN), 'UTF-16': (16, 'BOM'), 'UTF-32': (32, 'BOM')}
    UTF_BOM = {16: {BOM_UTF16_LE: 'UTF-16-LE', BOM_UTF16_BE: 'UTF-16-BE'}, 32: {BOM_UTF32_LE: 'UTF-32LE', BOM_UTF32_BE: 'UTF-32BE'}}
    SUFFIX_FORMAT = {'C': {8: {LITTLE_ENDIAN: '\x00', BIG_ENDIAN: '\x00'}, 16: {LITTLE_ENDIAN: '\x00\x00', BIG_ENDIAN: '\x00\x00'}, 32: {LITTLE_ENDIAN: '\x00\x00\x00\x00', BIG_ENDIAN: '\x00\x00\x00\x00'}}, 'UnixLine': {8: {LITTLE_ENDIAN: '\n', BIG_ENDIAN: '\n'}, 16: {LITTLE_ENDIAN: '\n\x00', BIG_ENDIAN: '\x00\n'}, 32: {LITTLE_ENDIAN: '\n\x00\x00\x00', BIG_ENDIAN: '\x00\x00\x00\n'}}}
    PASCAL_FORMATS = {'Pascal8': 1, 'Pascal16': 2, 'Pascal32': 4}
    _raw_value = None

    def __init__(self, parent, name, format, description=None, strip=None, charset=None, nbytes=None, truncate=None):
        Bytes.__init__(self, parent, name, 1, description)
        assert format in self.VALID_FORMATS
        self._format = format
        self._strip = strip
        self._truncate = truncate
        if not charset or charset in self.CHARSET_8BIT:
            self._character_size = 1
        elif charset in self.UTF_CHARSET:
            self._character_size = None
        else:
            raise FieldError('Invalid charset for %s: "%s"' % (self.path, charset))
        self._charset = charset
        if nbytes is not None:
            assert self._format == 'fixed'
            if not 1 <= nbytes <= 65535:
                raise FieldError('Invalid string size for %s: %s' % (self.path, nbytes))
            self._content_size = nbytes
            self._size = nbytes * 8
            self._content_offset = 0
        elif self._format in self.SUFFIX_FORMAT:
            self._content_offset = 0
            suffix = self.suffix_str
            length = self._parent.stream.searchBytesLength(suffix, False, self.absolute_address)
            if length is None:
                raise FieldError('Unable to find end of string %s (format %s)!' % (self.path, self._format))
            if 1 < len(suffix):
                length = alignValue(length, len(suffix))
            self._content_size = length
            self._size = (length + len(suffix)) * 8
        else:
            assert self._format in self.PASCAL_FORMATS
            prefix_size = self.PASCAL_FORMATS[self._format]
            self._content_offset = prefix_size
            value = self._parent.stream.readBits(self.absolute_address, prefix_size * 8, self._parent.endian)
            self._content_size = value
            self._size = (prefix_size + value) * 8
        if self._charset in self.UTF_CHARSET:
            (bomsize, endian) = self.UTF_CHARSET[self._charset]
            if endian == 'BOM':
                nbytes = bomsize // 8
                bom = self._parent.stream.readBytes(self.absolute_address, nbytes)
                bom_endian = self.UTF_BOM[bomsize]
                if bom not in bom_endian:
                    raise FieldError('String %s has invalid BOM (%s)!' % (self.path, repr(bom)))
                self._charset = bom_endian[bom]
                self._content_size -= nbytes
                self._content_offset += nbytes
        if self._character_size:
            self._length = self._content_size // self._character_size
        else:
            self._length = None
        return

    @staticmethod
    def staticSuffixStr(format, charset, endian):
        if format not in GenericString.SUFFIX_FORMAT:
            return ''
        suffix = GenericString.SUFFIX_FORMAT[format]
        if charset in GenericString.UTF_CHARSET:
            suffix_size = GenericString.UTF_CHARSET[charset][0]
            suffix = suffix[suffix_size]
        else:
            suffix = suffix[8]
        return suffix[endian]

    def _getSuffixStr(self):
        return self.staticSuffixStr(self._format, self._charset, self._parent.endian)

    suffix_str = property(_getSuffixStr)

    def _convertText(self, text):
        if not self._charset:
            self._charset = guessBytesCharset(text, default=FALLBACK_CHARSET)
        try:
            return unicode(text, self._charset, 'strict')
        except UnicodeDecodeError, err:
            pass

        if err.reason == 'truncated data' and err.end == len(text) and self._charset == 'UTF-16-LE':
            try:
                text = unicode(text + '\x00', self._charset, 'strict')
                self.warning('Fix truncated %s string: add missing nul byte' % self._charset)
                return text
            except UnicodeDecodeError, err:
                pass

        self.warning('Unable to convert string to Unicode: %s' % err)
        return unicode(text, FALLBACK_CHARSET, 'strict')

    def _guessCharset(self):
        addr = self.absolute_address + self._content_offset * 8
        bytes = self._parent.stream.readBytes(addr, self._content_size)
        return guessBytesCharset(bytes, default=FALLBACK_CHARSET)

    def createValue(self, human=True):
        if human:
            addr = self.absolute_address + self._content_offset * 8
            size = self._content_size
        else:
            addr = self.absolute_address
            size = self._size // 8
        if size == 0:
            return ''
        text = self._parent.stream.readBytes(addr, size)
        if not human:
            return text
        text = self._convertText(text)
        if self._truncate:
            pos = text.find(self._truncate)
            if 0 <= pos:
                text = text[:pos]
        if self._strip:
            if isinstance(self._strip, (str, unicode)):
                text = text.strip(self._strip)
            else:
                text = text.strip()
        assert isinstance(text, unicode)
        return text

    def createDisplay(self, human=True):
        if not human:
            if self._raw_value is None:
                self._raw_value = GenericString.createValue(self, False)
            value = makePrintable(self._raw_value, 'ASCII', to_unicode=True)
        elif self._charset:
            value = makePrintable(self.value, 'ISO-8859-1', to_unicode=True)
        else:
            value = self.value
        if config.max_string_length < len(value):
            value = '%s(...)' % value[:config.max_string_length]
        if not self._charset or not human:
            return makePrintable(value, 'ASCII', quote='"', to_unicode=True)
        elif value:
            return '"%s"' % value.replace('"', '\\"')
        else:
            return _('(empty)')
        return

    def createRawDisplay(self):
        return GenericString.createDisplay(self, human=False)

    def _getLength(self):
        if self._length is None:
            self._length = len(self.value)
        return self._length

    length = property(_getLength, doc='String length in characters')

    def _getFormat(self):
        return self._format

    format = property(_getFormat, doc="String format (eg. 'C')")

    def _getCharset(self):
        if not self._charset:
            self._charset = self._guessCharset()
        return self._charset

    charset = property(_getCharset, doc="String charset (eg. 'ISO-8859-1')")

    def _getContentSize(self):
        return self._content_size

    content_size = property(_getContentSize, doc='Content size in bytes')

    def _getContentOffset(self):
        return self._content_offset

    content_offset = property(_getContentOffset, doc='Content offset in bytes')

    def getFieldType(self):
        info = self.charset
        if self._strip:
            if isinstance(self._strip, (str, unicode)):
                info += ',strip=%s' % makePrintable(self._strip, 'ASCII', quote="'")
            else:
                info += ',strip=True'
        return '%s<%s>' % (Bytes.getFieldType(self), info)


def stringFactory(name, format, doc):

    class NewString(GenericString):
        __module__ = __name__
        __doc__ = doc

        def __init__(self, parent, name, description=None, strip=None, charset=None, truncate=None):
            GenericString.__init__(self, parent, name, format, description, strip=strip, charset=charset, truncate=truncate)

    cls = NewString
    cls.__name__ = name
    return cls


CString = stringFactory('CString', 'C', 'C string: string ending with nul byte.\nSee GenericString to get more information.')
UnixLine = stringFactory('UnixLine', 'UnixLine', 'Unix line: string ending with "\\n" (ASCII code 10).\nSee GenericString to get more information.')
PascalString8 = stringFactory('PascalString8', 'Pascal8', 'Pascal string: string prefixed with 8-bit integer containing its length (endian depends on parent endian).\nSee GenericString to get more information.')
PascalString16 = stringFactory('PascalString16', 'Pascal16', 'Pascal string: string prefixed with 16-bit integer containing its length (endian depends on parent endian).\nSee GenericString to get more information.')
PascalString32 = stringFactory('PascalString32', 'Pascal32', 'Pascal string: string prefixed with 32-bit integer containing its length (endian depends on parent endian).\nSee GenericString to get more information.')

class String(GenericString):
    """
    String with fixed size (size in bytes).
    See GenericString to get more information.
    """
    __module__ = __name__
    static_size = staticmethod(lambda *args, **kw: args[1] * 8)

    def __init__(self, parent, name, nbytes, description=None, strip=None, charset=None, truncate=None):
        GenericString.__init__(self, parent, name, 'fixed', description, strip=strip, charset=charset, nbytes=nbytes, truncate=truncate)


String.__name__ = 'FixedString'