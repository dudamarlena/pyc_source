# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/bs4/dammit.py
# Compiled at: 2013-03-18 16:15:18
"""Beautiful Soup bonus library: Unicode, Dammit

This class forces XML data into a standard format (usually to UTF-8 or
Unicode).  It is heavily based on code from Mark Pilgrim's Universal
Feed Parser. It does not rewrite the XML or HTML to reflect a new
encoding; that's the tree builder's job.
"""
import codecs
from htmlentitydefs import codepoint2name
import re, logging
chardet_type = None
try:
    import cchardet

    def chardet_dammit(s):
        return cchardet.detect(s)['encoding']


except ImportError:
    try:
        import chardet

        def chardet_dammit(s):
            return chardet.detect(s)['encoding']


    except ImportError:

        def chardet_dammit(s):
            return


try:
    import iconv_codec
except ImportError:
    pass

xml_encoding_re = re.compile(('^<\\?.*encoding=[\'"](.*?)[\'"].*\\?>').encode(), re.I)
html_meta_re = re.compile(('<\\s*meta[^>]+charset\\s*=\\s*["\']?([^>]*?)[ /;\'">]').encode(), re.I)

class EntitySubstitution(object):
    """Substitute XML or HTML entities for the corresponding characters."""

    def _populate_class_variables():
        lookup = {}
        reverse_lookup = {}
        characters_for_re = []
        for codepoint, name in list(codepoint2name.items()):
            character = unichr(codepoint)
            if codepoint != 34:
                characters_for_re.append(character)
                lookup[character] = name
            reverse_lookup[name] = character

        re_definition = '[%s]' % ('').join(characters_for_re)
        return (lookup, reverse_lookup, re.compile(re_definition))

    CHARACTER_TO_HTML_ENTITY, HTML_ENTITY_TO_CHARACTER, CHARACTER_TO_HTML_ENTITY_RE = _populate_class_variables()
    CHARACTER_TO_XML_ENTITY = {"'": 'apos', 
       '"': 'quot', 
       '&': 'amp', 
       '<': 'lt', 
       '>': 'gt'}
    BARE_AMPERSAND_OR_BRACKET = re.compile('([<>]|&(?!#\\d+;|#x[0-9a-fA-F]+;|\\w+;))')

    @classmethod
    def _substitute_html_entity(cls, matchobj):
        entity = cls.CHARACTER_TO_HTML_ENTITY.get(matchobj.group(0))
        return '&%s;' % entity

    @classmethod
    def _substitute_xml_entity(cls, matchobj):
        """Used with a regular expression to substitute the
        appropriate XML entity for an XML special character."""
        entity = cls.CHARACTER_TO_XML_ENTITY[matchobj.group(0)]
        return '&%s;' % entity

    @classmethod
    def quoted_attribute_value(self, value):
        """Make a value into a quoted XML attribute, possibly escaping it.

         Most strings will be quoted using double quotes.

          Bob's Bar -> "Bob's Bar"

         If a string contains double quotes, it will be quoted using
         single quotes.

          Welcome to "my bar" -> 'Welcome to "my bar"'

         If a string contains both single and double quotes, the
         double quotes will be escaped, and the string will be quoted
         using double quotes.

          Welcome to "Bob's Bar" -> "Welcome to &quot;Bob's bar&quot;
        """
        quote_with = '"'
        if '"' in value:
            if "'" in value:
                replace_with = '&quot;'
                value = value.replace('"', replace_with)
            else:
                quote_with = "'"
        return quote_with + value + quote_with

    @classmethod
    def substitute_xml(cls, value, make_quoted_attribute=False):
        """Substitute XML entities for special XML characters.

        :param value: A string to be substituted. The less-than sign will
          become &lt;, the greater-than sign will become &gt;, and any
          ampersands that are not part of an entity defition will
          become &amp;.

        :param make_quoted_attribute: If True, then the string will be
         quoted, as befits an attribute value.
        """
        value = cls.BARE_AMPERSAND_OR_BRACKET.sub(cls._substitute_xml_entity, value)
        if make_quoted_attribute:
            value = cls.quoted_attribute_value(value)
        return value

    @classmethod
    def substitute_html(cls, s):
        """Replace certain Unicode characters with named HTML entities.

        This differs from data.encode(encoding, 'xmlcharrefreplace')
        in that the goal is to make the result more readable (to those
        with ASCII displays) rather than to recover from
        errors. There's absolutely nothing wrong with a UTF-8 string
        containg a LATIN SMALL LETTER E WITH ACUTE, but replacing that
        character with "&eacute;" will make it more readable to some
        people.
        """
        return cls.CHARACTER_TO_HTML_ENTITY_RE.sub(cls._substitute_html_entity, s)


class UnicodeDammit:
    """A class for detecting the encoding of a *ML document and
    converting it to a Unicode string. If the source encoding is
    windows-1252, can replace MS smart quotes with their HTML or XML
    equivalents."""
    CHARSET_ALIASES = {'macintosh': 'mac-roman', 'x-sjis': 'shift-jis'}
    ENCODINGS_WITH_SMART_QUOTES = [
     'windows-1252',
     'iso-8859-1',
     'iso-8859-2']

    def __init__(self, markup, override_encodings=[], smart_quotes_to=None, is_html=False):
        self.declared_html_encoding = None
        self.smart_quotes_to = smart_quotes_to
        self.tried_encodings = []
        self.contains_replacement_characters = False
        if markup == '' or isinstance(markup, unicode):
            self.markup = markup
            self.unicode_markup = unicode(markup)
            self.original_encoding = None
            return
        else:
            new_markup, document_encoding, sniffed_encoding = self._detectEncoding(markup, is_html)
            self.markup = new_markup
            u = None
            if new_markup != markup:
                u = self._convert_from('utf8')
                self.original_encoding = sniffed_encoding
            if not u:
                for proposed_encoding in override_encodings + [document_encoding, sniffed_encoding]:
                    if proposed_encoding is not None:
                        u = self._convert_from(proposed_encoding)
                        if u:
                            break

            if not u and not isinstance(self.markup, unicode):
                u = self._convert_from(chardet_dammit(self.markup))
            if not u:
                for proposed_encoding in ('utf-8', 'windows-1252'):
                    u = self._convert_from(proposed_encoding)
                    if u:
                        break

            if not u:
                for proposed_encoding in override_encodings + [
                 document_encoding, sniffed_encoding, 'utf-8', 'windows-1252']:
                    if proposed_encoding != 'ascii':
                        u = self._convert_from(proposed_encoding, 'replace')
                    if u is not None:
                        logging.warning('Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.')
                        self.contains_replacement_characters = True
                        break

            self.unicode_markup = u
            if not u:
                self.original_encoding = None
            return

    def _sub_ms_char(self, match):
        """Changes a MS smart quote character to an XML or HTML
        entity, or an ASCII character."""
        orig = match.group(1)
        if self.smart_quotes_to == 'ascii':
            sub = self.MS_CHARS_TO_ASCII.get(orig).encode()
        else:
            sub = self.MS_CHARS.get(orig)
            if type(sub) == tuple:
                if self.smart_quotes_to == 'xml':
                    sub = ('&#x').encode() + sub[1].encode() + (';').encode()
                else:
                    sub = ('&').encode() + sub[0].encode() + (';').encode()
            else:
                sub = sub.encode()
        return sub

    def _convert_from(self, proposed, errors='strict'):
        proposed = self.find_codec(proposed)
        if not proposed or (proposed, errors) in self.tried_encodings:
            return
        self.tried_encodings.append((proposed, errors))
        markup = self.markup
        if self.smart_quotes_to is not None and proposed.lower() in self.ENCODINGS_WITH_SMART_QUOTES:
            smart_quotes_re = b'([\x80-\x9f])'
            smart_quotes_compiled = re.compile(smart_quotes_re)
            markup = smart_quotes_compiled.sub(self._sub_ms_char, markup)
        try:
            u = self._to_unicode(markup, proposed, errors)
            self.markup = u
            self.original_encoding = proposed
        except Exception as e:
            return

        return self.markup

    def _to_unicode(self, data, encoding, errors='strict'):
        """Given a string and its encoding, decodes the string into Unicode.
        %encoding is a string recognized by encodings.aliases"""
        if len(data) >= 4 and data[:2] == b'\xfe\xff' and data[2:4] != '\x00\x00':
            encoding = 'utf-16be'
            data = data[2:]
        elif len(data) >= 4 and data[:2] == b'\xff\xfe' and data[2:4] != '\x00\x00':
            encoding = 'utf-16le'
            data = data[2:]
        elif data[:3] == '\ufeff':
            encoding = 'utf-8'
            data = data[3:]
        elif data[:4] == b'\x00\x00\xfe\xff':
            encoding = 'utf-32be'
            data = data[4:]
        elif data[:4] == b'\xff\xfe\x00\x00':
            encoding = 'utf-32le'
            data = data[4:]
        newdata = unicode(data, encoding, errors)
        return newdata

    def _detectEncoding(self, xml_data, is_html=False):
        """Given a document, tries to detect its XML encoding."""
        xml_encoding = sniffed_xml_encoding = None
        try:
            if xml_data[:4] == b'Lo\xa7\x94':
                xml_data = self._ebcdic_to_ascii(xml_data)
            elif xml_data[:4] == '\x00<\x00?':
                sniffed_xml_encoding = 'utf-16be'
                xml_data = unicode(xml_data, 'utf-16be').encode('utf-8')
            elif len(xml_data) >= 4 and xml_data[:2] == b'\xfe\xff' and xml_data[2:4] != '\x00\x00':
                sniffed_xml_encoding = 'utf-16be'
                xml_data = unicode(xml_data[2:], 'utf-16be').encode('utf-8')
            elif xml_data[:4] == '<\x00?\x00':
                sniffed_xml_encoding = 'utf-16le'
                xml_data = unicode(xml_data, 'utf-16le').encode('utf-8')
            elif len(xml_data) >= 4 and xml_data[:2] == b'\xff\xfe' and xml_data[2:4] != '\x00\x00':
                sniffed_xml_encoding = 'utf-16le'
                xml_data = unicode(xml_data[2:], 'utf-16le').encode('utf-8')
            elif xml_data[:4] == '\x00\x00\x00<':
                sniffed_xml_encoding = 'utf-32be'
                xml_data = unicode(xml_data, 'utf-32be').encode('utf-8')
            elif xml_data[:4] == '<\x00\x00\x00':
                sniffed_xml_encoding = 'utf-32le'
                xml_data = unicode(xml_data, 'utf-32le').encode('utf-8')
            elif xml_data[:4] == b'\x00\x00\xfe\xff':
                sniffed_xml_encoding = 'utf-32be'
                xml_data = unicode(xml_data[4:], 'utf-32be').encode('utf-8')
            elif xml_data[:4] == b'\xff\xfe\x00\x00':
                sniffed_xml_encoding = 'utf-32le'
                xml_data = unicode(xml_data[4:], 'utf-32le').encode('utf-8')
            elif xml_data[:3] == '\ufeff':
                sniffed_xml_encoding = 'utf-8'
                xml_data = unicode(xml_data[3:], 'utf-8').encode('utf-8')
            else:
                sniffed_xml_encoding = 'ascii'
        except:
            xml_encoding_match = None

        xml_encoding_match = xml_encoding_re.match(xml_data)
        if not xml_encoding_match and is_html:
            xml_encoding_match = html_meta_re.search(xml_data)
        if xml_encoding_match is not None:
            xml_encoding = xml_encoding_match.groups()[0].decode('ascii').lower()
            if is_html:
                self.declared_html_encoding = xml_encoding
            if sniffed_xml_encoding and xml_encoding in ('iso-10646-ucs-2', 'ucs-2',
                                                         'csunicode', 'iso-10646-ucs-4',
                                                         'ucs-4', 'csucs4', 'utf-16',
                                                         'utf-32', 'utf_16', 'utf_32',
                                                         'utf16', 'u16'):
                xml_encoding = sniffed_xml_encoding
        return (
         xml_data, xml_encoding, sniffed_xml_encoding)

    def find_codec(self, charset):
        return self._codec(self.CHARSET_ALIASES.get(charset, charset)) or charset and self._codec(charset.replace('-', '')) or charset and self._codec(charset.replace('-', '_')) or charset

    def _codec(self, charset):
        if not charset:
            return charset
        else:
            codec = None
            try:
                codecs.lookup(charset)
                codec = charset
            except (LookupError, ValueError):
                pass

            return codec

    EBCDIC_TO_ASCII_MAP = None

    def _ebcdic_to_ascii(self, s):
        c = self.__class__
        if not c.EBCDIC_TO_ASCII_MAP:
            emap = (0, 1, 2, 3, 156, 9, 134, 127, 151, 141, 142, 11, 12, 13, 14, 15,
                    16, 17, 18, 19, 157, 133, 8, 135, 24, 25, 146, 143, 28, 29, 30,
                    31, 128, 129, 130, 131, 132, 10, 23, 27, 136, 137, 138, 139,
                    140, 5, 6, 7, 144, 145, 22, 147, 148, 149, 150, 4, 152, 153,
                    154, 155, 20, 21, 158, 26, 32, 160, 161, 162, 163, 164, 165,
                    166, 167, 168, 91, 46, 60, 40, 43, 33, 38, 169, 170, 171, 172,
                    173, 174, 175, 176, 177, 93, 36, 42, 41, 59, 94, 45, 47, 178,
                    179, 180, 181, 182, 183, 184, 185, 124, 44, 37, 95, 62, 63, 186,
                    187, 188, 189, 190, 191, 192, 193, 194, 96, 58, 35, 64, 39, 61,
                    34, 195, 97, 98, 99, 100, 101, 102, 103, 104, 105, 196, 197,
                    198, 199, 200, 201, 202, 106, 107, 108, 109, 110, 111, 112, 113,
                    114, 203, 204, 205, 206, 207, 208, 209, 126, 115, 116, 117, 118,
                    119, 120, 121, 122, 210, 211, 212, 213, 214, 215, 216, 217, 218,
                    219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231,
                    123, 65, 66, 67, 68, 69, 70, 71, 72, 73, 232, 233, 234, 235,
                    236, 237, 125, 74, 75, 76, 77, 78, 79, 80, 81, 82, 238, 239,
                    240, 241, 242, 243, 92, 159, 83, 84, 85, 86, 87, 88, 89, 90,
                    244, 245, 246, 247, 248, 249, 48, 49, 50, 51, 52, 53, 54, 55,
                    56, 57, 250, 251, 252, 253, 254, 255)
            import string
            c.EBCDIC_TO_ASCII_MAP = string.maketrans(('').join(map(chr, list(range(256)))), ('').join(map(chr, emap)))
        return s.translate(c.EBCDIC_TO_ASCII_MAP)

    MS_CHARS = {b'\x80': ('euro', '20AC'), b'\x81': ' ', 
       b'\x82': ('sbquo', '201A'), 
       b'\x83': ('fnof', '192'), 
       b'\x84': ('bdquo', '201E'), 
       b'\x85': ('hellip', '2026'), 
       b'\x86': ('dagger', '2020'), 
       b'\x87': ('Dagger', '2021'), 
       b'\x88': ('circ', '2C6'), 
       b'\x89': ('permil', '2030'), 
       b'\x8a': ('Scaron', '160'), 
       b'\x8b': ('lsaquo', '2039'), 
       b'\x8c': ('OElig', '152'), 
       b'\x8d': '?', 
       b'\x8e': ('#x17D', '17D'), 
       b'\x8f': '?', 
       b'\x90': '?', 
       b'\x91': ('lsquo', '2018'), 
       b'\x92': ('rsquo', '2019'), 
       b'\x93': ('ldquo', '201C'), 
       b'\x94': ('rdquo', '201D'), 
       b'\x95': ('bull', '2022'), 
       b'\x96': ('ndash', '2013'), 
       b'\x97': ('mdash', '2014'), 
       b'\x98': ('tilde', '2DC'), 
       b'\x99': ('trade', '2122'), 
       b'\x9a': ('scaron', '161'), 
       b'\x9b': ('rsaquo', '203A'), 
       b'\x9c': ('oelig', '153'), 
       b'\x9d': '?', 
       b'\x9e': ('#x17E', '17E'), 
       b'\x9f': ('Yuml', '')}
    MS_CHARS_TO_ASCII = {b'\x80': 'EUR', 
       b'\x81': ' ', 
       b'\x82': ',', 
       b'\x83': 'f', 
       b'\x84': ',,', 
       b'\x85': '...', 
       b'\x86': '+', 
       b'\x87': '++', 
       b'\x88': '^', 
       b'\x89': '%', 
       b'\x8a': 'S', 
       b'\x8b': '<', 
       b'\x8c': 'OE', 
       b'\x8d': '?', 
       b'\x8e': 'Z', 
       b'\x8f': '?', 
       b'\x90': '?', 
       b'\x91': "'", 
       b'\x92': "'", 
       b'\x93': '"', 
       b'\x94': '"', 
       b'\x95': '*', 
       b'\x96': '-', 
       b'\x97': '--', 
       b'\x98': '~', 
       b'\x99': '(TM)', 
       b'\x9a': 's', 
       b'\x9b': '>', 
       b'\x9c': 'oe', 
       b'\x9d': '?', 
       b'\x9e': 'z', 
       b'\x9f': 'Y', 
       b'\xa0': ' ', 
       b'\xa1': '!', 
       b'\xa2': 'c', 
       b'\xa3': 'GBP', 
       b'\xa4': '$', 
       b'\xa5': 'YEN', 
       b'\xa6': '|', 
       b'\xa7': 'S', 
       b'\xa8': '..', 
       b'\xa9': '', 
       b'\xaa': '(th)', 
       b'\xab': '<<', 
       b'\xac': '!', 
       b'\xad': ' ', 
       b'\xae': '(R)', 
       b'\xaf': '-', 
       b'\xb0': 'o', 
       b'\xb1': '+-', 
       b'\xb2': '2', 
       b'\xb3': '3', 
       b'\xb4': ("'", 'acute'), 
       b'\xb5': 'u', 
       b'\xb6': 'P', 
       b'\xb7': '*', 
       b'\xb8': ',', 
       b'\xb9': '1', 
       b'\xba': '(th)', 
       b'\xbb': '>>', 
       b'\xbc': '1/4', 
       b'\xbd': '1/2', 
       b'\xbe': '3/4', 
       b'\xbf': '?', 
       b'\xc0': 'A', 
       b'\xc1': 'A', 
       b'\xc2': 'A', 
       b'\xc3': 'A', 
       b'\xc4': 'A', 
       b'\xc5': 'A', 
       b'\xc6': 'AE', 
       b'\xc7': 'C', 
       b'\xc8': 'E', 
       b'\xc9': 'E', 
       b'\xca': 'E', 
       b'\xcb': 'E', 
       b'\xcc': 'I', 
       b'\xcd': 'I', 
       b'\xce': 'I', 
       b'\xcf': 'I', 
       b'\xd0': 'D', 
       b'\xd1': 'N', 
       b'\xd2': 'O', 
       b'\xd3': 'O', 
       b'\xd4': 'O', 
       b'\xd5': 'O', 
       b'\xd6': 'O', 
       b'\xd7': '*', 
       b'\xd8': 'O', 
       b'\xd9': 'U', 
       b'\xda': 'U', 
       b'\xdb': 'U', 
       b'\xdc': 'U', 
       b'\xdd': 'Y', 
       b'\xde': 'b', 
       b'\xdf': 'B', 
       b'\xe0': 'a', 
       b'\xe1': 'a', 
       b'\xe2': 'a', 
       b'\xe3': 'a', 
       b'\xe4': 'a', 
       b'\xe5': 'a', 
       b'\xe6': 'ae', 
       b'\xe7': 'c', 
       b'\xe8': 'e', 
       b'\xe9': 'e', 
       b'\xea': 'e', 
       b'\xeb': 'e', 
       b'\xec': 'i', 
       b'\xed': 'i', 
       b'\xee': 'i', 
       b'\xef': 'i', 
       b'\xf0': 'o', 
       b'\xf1': 'n', 
       b'\xf2': 'o', 
       b'\xf3': 'o', 
       b'\xf4': 'o', 
       b'\xf5': 'o', 
       b'\xf6': 'o', 
       b'\xf7': '/', 
       b'\xf8': 'o', 
       b'\xf9': 'u', 
       b'\xfa': 'u', 
       b'\xfb': 'u', 
       b'\xfc': 'u', 
       b'\xfd': 'y', 
       b'\xfe': 'b', 
       b'\xff': 'y'}
    WINDOWS_1252_TO_UTF8 = {128: '€', 
       130: '‚', 
       131: 'ƒ', 
       132: '„', 
       133: '…', 
       134: '†', 
       135: '‡', 
       136: 'ˆ', 
       137: '‰', 
       138: 'Š', 
       139: '‹', 
       140: 'Œ', 
       142: 'Ž', 
       145: '‘', 
       146: '’', 
       147: '“', 
       148: '”', 
       149: '•', 
       150: '–', 
       151: '—', 
       152: '˜', 
       153: '™', 
       154: 'š', 
       155: '›', 
       156: 'œ', 
       158: 'ž', 
       159: 'Ÿ', 
       160: '\xa0', 
       161: '¡', 
       162: '¢', 
       163: '£', 
       164: '¤', 
       165: '¥', 
       166: '¦', 
       167: '§', 
       168: '¨', 
       169: '©', 
       170: 'ª', 
       171: '«', 
       172: '¬', 
       173: '\xad', 
       174: '®', 
       175: '¯', 
       176: '°', 
       177: '±', 
       178: '²', 
       179: '³', 
       180: '´', 
       181: 'µ', 
       182: '¶', 
       183: '·', 
       184: '¸', 
       185: '¹', 
       186: 'º', 
       187: '»', 
       188: '¼', 
       189: '½', 
       190: '¾', 
       191: '¿', 
       192: 'À', 
       193: 'Á', 
       194: 'Â', 
       195: 'Ã', 
       196: 'Ä', 
       197: 'Å', 
       198: 'Æ', 
       199: 'Ç', 
       200: 'È', 
       201: 'É', 
       202: 'Ê', 
       203: 'Ë', 
       204: 'Ì', 
       205: 'Í', 
       206: 'Î', 
       207: 'Ï', 
       208: 'Ð', 
       209: 'Ñ', 
       210: 'Ò', 
       211: 'Ó', 
       212: 'Ô', 
       213: 'Õ', 
       214: 'Ö', 
       215: '×', 
       216: 'Ø', 
       217: 'Ù', 
       218: 'Ú', 
       219: 'Û', 
       220: 'Ü', 
       221: 'Ý', 
       222: 'Þ', 
       223: 'ß', 
       224: 'à', 
       225: b'\xa1', 
       226: 'â', 
       227: 'ã', 
       228: 'ä', 
       229: 'å', 
       230: 'æ', 
       231: 'ç', 
       232: 'è', 
       233: 'é', 
       234: 'ê', 
       235: 'ë', 
       236: 'ì', 
       237: 'í', 
       238: 'î', 
       239: 'ï', 
       240: 'ð', 
       241: 'ñ', 
       242: 'ò', 
       243: 'ó', 
       244: 'ô', 
       245: 'õ', 
       246: 'ö', 
       247: '÷', 
       248: 'ø', 
       249: 'ù', 
       250: 'ú', 
       251: 'û', 
       252: 'ü', 
       253: 'ý', 
       254: 'þ'}
    MULTIBYTE_MARKERS_AND_SIZES = [
     (194, 223, 2),
     (224, 239, 3),
     (240, 244, 4)]
    FIRST_MULTIBYTE_MARKER = MULTIBYTE_MARKERS_AND_SIZES[0][0]
    LAST_MULTIBYTE_MARKER = MULTIBYTE_MARKERS_AND_SIZES[(-1)][1]

    @classmethod
    def detwingle(cls, in_bytes, main_encoding='utf8', embedded_encoding='windows-1252'):
        """Fix characters from one encoding embedded in some other encoding.

        Currently the only situation supported is Windows-1252 (or its
        subset ISO-8859-1), embedded in UTF-8.

        The input must be a bytestring. If you've already converted
        the document to Unicode, you're too late.

        The output is a bytestring in which `embedded_encoding`
        characters have been converted to their `main_encoding`
        equivalents.
        """
        if embedded_encoding.replace('_', '-').lower() not in ('windows-1252', 'windows_1252'):
            raise NotImplementedError('Windows-1252 and ISO-8859-1 are the only currently supported embedded encodings.')
        if main_encoding.lower() not in ('utf8', 'utf-8'):
            raise NotImplementedError('UTF-8 is the only currently supported main encoding.')
        byte_chunks = []
        chunk_start = 0
        pos = 0
        while pos < len(in_bytes):
            byte = in_bytes[pos]
            if not isinstance(byte, int):
                byte = ord(byte)
            if byte >= cls.FIRST_MULTIBYTE_MARKER and byte <= cls.LAST_MULTIBYTE_MARKER:
                for start, end, size in cls.MULTIBYTE_MARKERS_AND_SIZES:
                    if byte >= start and byte <= end:
                        pos += size
                        break

            elif byte >= 128 and byte in cls.WINDOWS_1252_TO_UTF8:
                byte_chunks.append(in_bytes[chunk_start:pos])
                byte_chunks.append(cls.WINDOWS_1252_TO_UTF8[byte])
                pos += 1
                chunk_start = pos
            else:
                pos += 1

        if chunk_start == 0:
            return in_bytes
        byte_chunks.append(in_bytes[chunk_start:])
        return ('').join(byte_chunks)