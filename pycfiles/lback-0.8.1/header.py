# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: email\header.pyc
# Compiled at: 2009-12-06 23:02:40
"""Header encoding and decoding functionality."""
__all__ = [
 'Header',
 'decode_header',
 'make_header']
import re, binascii, email.quoprimime, email.base64mime
from email.errors import HeaderParseError
from email.charset import Charset
NL = '\n'
SPACE = ' '
USPACE = ' '
SPACE8 = ' ' * 8
UEMPTYSTRING = ''
MAXLINELEN = 76
USASCII = Charset('us-ascii')
UTF8 = Charset('utf-8')
ecre = re.compile('\n  =\\?                   # literal =?\n  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset\n  \\?                    # literal ?\n  (?P<encoding>[qb])    # either a "q" or a "b", case insensitive\n  \\?                    # literal ?\n  (?P<encoded>.*?)      # non-greedy up to the next ?= is the encoded string\n  \\?=                   # literal ?=\n  (?=[ \\t]|$)           # whitespace or the end of the string\n  ', re.VERBOSE | re.IGNORECASE | re.MULTILINE)
fcre = re.compile('[\\041-\\176]+:$')
_max_append = email.quoprimime._max_append

def decode_header(header):
    """Decode a message header value without converting charset.

    Returns a list of (decoded_string, charset) pairs containing each of the
    decoded parts of the header.  Charset is None for non-encoded parts of the
    header, otherwise a lower-case string containing the name of the character
    set specified in the encoded string.

    An email.errors.HeaderParseError may be raised when certain decoding error
    occurs (e.g. a base64 decoding exception).
    """
    header = str(header)
    if not ecre.search(header):
        return [(header, None)]
    else:
        decoded = []
        dec = ''
        for line in header.splitlines():
            if not ecre.search(line):
                decoded.append((line, None))
                continue
            parts = ecre.split(line)
            while parts:
                unenc = parts.pop(0).strip()
                if unenc:
                    if decoded and decoded[(-1)][1] is None:
                        decoded[-1] = (
                         decoded[(-1)][0] + SPACE + unenc, None)
                    else:
                        decoded.append((unenc, None))
                if parts:
                    charset, encoding = [ s.lower() for s in parts[0:2] ]
                    encoded = parts[2]
                    dec = None
                    if encoding == 'q':
                        dec = email.quoprimime.header_decode(encoded)
                    elif encoding == 'b':
                        try:
                            dec = email.base64mime.decode(encoded)
                        except binascii.Error:
                            raise HeaderParseError

                    if dec is None:
                        dec = encoded
                    if decoded and decoded[(-1)][1] == charset:
                        decoded[-1] = (
                         decoded[(-1)][0] + dec, decoded[(-1)][1])
                    else:
                        decoded.append((dec, charset))
                del parts[0:3]

        return decoded


def make_header(decoded_seq, maxlinelen=None, header_name=None, continuation_ws=' '):
    """Create a Header from a sequence of pairs as returned by decode_header()

    decode_header() takes a header value string and returns a sequence of
    pairs of the format (decoded_string, charset) where charset is the string
    name of the character set.

    This function takes one of those sequence of pairs and returns a Header
    instance.  Optional maxlinelen, header_name, and continuation_ws are as in
    the Header constructor.
    """
    h = Header(maxlinelen=maxlinelen, header_name=header_name, continuation_ws=continuation_ws)
    for s, charset in decoded_seq:
        if charset is not None and not isinstance(charset, Charset):
            charset = Charset(charset)
        h.append(s, charset)

    return h


class Header():

    def __init__(self, s=None, charset=None, maxlinelen=None, header_name=None, continuation_ws=' ', errors='strict'):
        """Create a MIME-compliant header that can contain many character sets.

        Optional s is the initial header value.  If None, the initial header
        value is not set.  You can later append to the header with .append()
        method calls.  s may be a byte string or a Unicode string, but see the
        .append() documentation for semantics.

        Optional charset serves two purposes: it has the same meaning as the
        charset argument to the .append() method.  It also sets the default
        character set for all subsequent .append() calls that omit the charset
        argument.  If charset is not provided in the constructor, the us-ascii
        charset is used both as s's initial charset and as the default for
        subsequent .append() calls.

        The maximum line length can be specified explicit via maxlinelen.  For
        splitting the first line to a shorter value (to account for the field
        header which isn't included in s, e.g. `Subject') pass in the name of
        the field in header_name.  The default maxlinelen is 76.

        continuation_ws must be RFC 2822 compliant folding whitespace (usually
        either a space or a hard tab) which will be prepended to continuation
        lines.

        errors is passed through to the .append() call.
        """
        if charset is None:
            charset = USASCII
        if not isinstance(charset, Charset):
            charset = Charset(charset)
        self._charset = charset
        self._continuation_ws = continuation_ws
        cws_expanded_len = len(continuation_ws.replace('\t', SPACE8))
        self._chunks = []
        if s is not None:
            self.append(s, charset, errors)
        if maxlinelen is None:
            maxlinelen = MAXLINELEN
        if header_name is None:
            self._firstlinelen = maxlinelen
        else:
            self._firstlinelen = maxlinelen - len(header_name) - 2
        self._maxlinelen = maxlinelen - cws_expanded_len
        return

    def __str__(self):
        """A synonym for self.encode()."""
        return self.encode()

    def __unicode__(self):
        """Helper for the built-in unicode function."""
        uchunks = []
        lastcs = None
        for s, charset in self._chunks:
            nextcs = charset
            if uchunks:
                if lastcs not in (None, 'us-ascii'):
                    if nextcs in (None, 'us-ascii'):
                        uchunks.append(USPACE)
                        nextcs = None
                elif nextcs not in (None, 'us-ascii'):
                    uchunks.append(USPACE)
            lastcs = nextcs
            uchunks.append(unicode(s, str(charset)))

        return UEMPTYSTRING.join(uchunks)

    def __eq__(self, other):
        return other == self.encode()

    def __ne__(self, other):
        return not self == other

    def append--- This code section failed: ---

 L. 247         0  LOAD_FAST             2  'charset'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_FALSE    24  'to 24'

 L. 248        12  LOAD_FAST             0  'self'
               15  LOAD_ATTR             1  '_charset'
               18  STORE_FAST            2  'charset'
               21  JUMP_FORWARD         30  'to 54'

 L. 249        24  LOAD_GLOBAL           2  'isinstance'
               27  LOAD_FAST             2  'charset'
               30  LOAD_GLOBAL           3  'Charset'
               33  CALL_FUNCTION_2       2  None
               36  POP_JUMP_IF_TRUE     54  'to 54'

 L. 250        39  LOAD_GLOBAL           3  'Charset'
               42  LOAD_FAST             2  'charset'
               45  CALL_FUNCTION_1       1  None
               48  STORE_FAST            2  'charset'
               51  JUMP_FORWARD          0  'to 54'
             54_0  COME_FROM            51  '51'
             54_1  COME_FROM            21  '21'

 L. 252        54  LOAD_FAST             2  'charset'
               57  LOAD_CONST               '8bit'
               60  COMPARE_OP            3  !=
               63  POP_JUMP_IF_FALSE   268  'to 268'

 L. 256        66  LOAD_GLOBAL           2  'isinstance'
               69  LOAD_FAST             1  's'
               72  LOAD_GLOBAL           4  'str'
               75  CALL_FUNCTION_2       2  None
               78  POP_JUMP_IF_FALSE   148  'to 148'

 L. 259        81  LOAD_FAST             2  'charset'
               84  LOAD_ATTR             5  'input_codec'
               87  JUMP_IF_TRUE_OR_POP    93  'to 93'
               90  LOAD_CONST               'us-ascii'
             93_0  COME_FROM            87  '87'
               93  STORE_FAST            4  'incodec'

 L. 260        96  LOAD_GLOBAL           6  'unicode'
               99  LOAD_FAST             1  's'
              102  LOAD_FAST             4  'incodec'
              105  LOAD_FAST             3  'errors'
              108  CALL_FUNCTION_3       3  None
              111  STORE_FAST            5  'ustr'

 L. 264       114  LOAD_FAST             2  'charset'
              117  LOAD_ATTR             7  'output_codec'
              120  JUMP_IF_TRUE_OR_POP   126  'to 126'
              123  LOAD_CONST               'us-ascii'
            126_0  COME_FROM           120  '120'
              126  STORE_FAST            6  'outcodec'

 L. 265       129  LOAD_FAST             5  'ustr'
              132  LOAD_ATTR             8  'encode'
              135  LOAD_FAST             6  'outcodec'
              138  LOAD_FAST             3  'errors'
              141  CALL_FUNCTION_2       2  None
              144  POP_TOP          
              145  JUMP_ABSOLUTE       268  'to 268'

 L. 266       148  LOAD_GLOBAL           2  'isinstance'
              151  LOAD_FAST             1  's'
              154  LOAD_GLOBAL           6  'unicode'
              157  CALL_FUNCTION_2       2  None
              160  POP_JUMP_IF_FALSE   268  'to 268'

 L. 270       163  SETUP_LOOP           99  'to 265'
              166  LOAD_GLOBAL           9  'USASCII'
              169  LOAD_FAST             2  'charset'
              172  LOAD_GLOBAL          10  'UTF8'
              175  BUILD_TUPLE_3         3 
              178  GET_ITER         
              179  FOR_ITER             64  'to 246'
              182  STORE_FAST            2  'charset'

 L. 271       185  SETUP_EXCEPT         38  'to 226'

 L. 272       188  LOAD_FAST             2  'charset'
              191  LOAD_ATTR             7  'output_codec'
              194  JUMP_IF_TRUE_OR_POP   200  'to 200'
              197  LOAD_CONST               'us-ascii'
            200_0  COME_FROM           194  '194'
              200  STORE_FAST            6  'outcodec'

 L. 273       203  LOAD_FAST             1  's'
              206  LOAD_ATTR             8  'encode'
              209  LOAD_FAST             6  'outcodec'
              212  LOAD_FAST             3  'errors'
              215  CALL_FUNCTION_2       2  None
              218  STORE_FAST            1  's'

 L. 274       221  BREAK_LOOP       
              222  POP_BLOCK        
              223  JUMP_BACK           179  'to 179'
            226_0  COME_FROM           185  '185'

 L. 275       226  DUP_TOP          
              227  LOAD_GLOBAL          11  'UnicodeError'
              230  COMPARE_OP           10  exception-match
              233  POP_JUMP_IF_FALSE   242  'to 242'
              236  POP_TOP          
              237  POP_TOP          
              238  POP_TOP          

 L. 276       239  JUMP_BACK           179  'to 179'
              242  END_FINALLY      
            243_0  COME_FROM           242  '242'
              243  JUMP_BACK           179  'to 179'
              246  POP_BLOCK        

 L. 278       247  LOAD_GLOBAL          12  'False'
              250  POP_JUMP_IF_TRUE    265  'to 265'
              253  LOAD_ASSERT              AssertionError
              256  LOAD_CONST               'utf-8 conversion failed'
              259  RAISE_VARARGS_2       2  None
            262_0  COME_FROM           163  '163'
              262  JUMP_ABSOLUTE       268  'to 268'
              265  JUMP_FORWARD          0  'to 268'
            268_0  COME_FROM           265  '265'

 L. 279       268  LOAD_FAST             0  'self'
              271  LOAD_ATTR            14  '_chunks'
              274  LOAD_ATTR            15  'append'
              277  LOAD_FAST             1  's'
              280  LOAD_FAST             2  'charset'
              283  BUILD_TUPLE_2         2 
              286  CALL_FUNCTION_1       1  None
              289  POP_TOP          
              290  LOAD_CONST               None
              293  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 262

    def _split(self, s, charset, maxlinelen, splitchars):
        splittable = charset.to_splittable(s)
        encoded = charset.from_splittable(splittable, True)
        elen = charset.encoded_header_len(encoded)
        if elen <= maxlinelen:
            return [(encoded, charset)]
        if charset == '8bit':
            return [(s, charset)]
        if charset == 'us-ascii':
            return self._split_ascii(s, charset, maxlinelen, splitchars)
        if elen == len(s):
            splitpnt = maxlinelen
            first = charset.from_splittable(splittable[:splitpnt], False)
            last = charset.from_splittable(splittable[splitpnt:], False)
        else:
            first, last = _binsplit(splittable, charset, maxlinelen)
        fsplittable = charset.to_splittable(first)
        fencoded = charset.from_splittable(fsplittable, True)
        chunk = [(fencoded, charset)]
        return chunk + self._split(last, charset, self._maxlinelen, splitchars)

    def _split_ascii(self, s, charset, firstlen, splitchars):
        chunks = _split_ascii(s, firstlen, self._maxlinelen, self._continuation_ws, splitchars)
        return zip(chunks, [charset] * len(chunks))

    def _encode_chunks(self, newchunks, maxlinelen):
        chunks = []
        for header, charset in newchunks:
            if not header:
                continue
            if charset is None or charset.header_encoding is None:
                s = header
            else:
                s = charset.header_encode(header)
            if chunks and chunks[(-1)].endswith(' '):
                extra = ''
            else:
                extra = ' '
            _max_append(chunks, s, maxlinelen, extra)

        joiner = NL + self._continuation_ws
        return joiner.join(chunks)

    def encode(self, splitchars=';, '):
        """Encode a message header into an RFC-compliant format.

        There are many issues involved in converting a given string for use in
        an email header.  Only certain character sets are readable in most
        email clients, and as header strings can only contain a subset of
        7-bit ASCII, care must be taken to properly convert and encode (with
        Base64 or quoted-printable) header strings.  In addition, there is a
        75-character length limit on any given encoded header field, so
        line-wrapping must be performed, even with double-byte character sets.

        This method will do its best to convert the string to the correct
        character set used in email, and encode and line wrap it safely with
        the appropriate scheme for that character set.

        If the given charset is not known or an error occurs during
        conversion, this function will return the header untouched.

        Optional splitchars is a string containing characters to split long
        ASCII lines on, in rough support of RFC 2822's `highest level
        syntactic breaks'.  This doesn't affect RFC 2047 encoded lines.
        """
        newchunks = []
        maxlinelen = self._firstlinelen
        lastlen = 0
        for s, charset in self._chunks:
            targetlen = maxlinelen - lastlen - 1
            if targetlen < charset.encoded_header_len(''):
                targetlen = maxlinelen
            newchunks += self._split(s, charset, targetlen, splitchars)
            lastchunk, lastcharset = newchunks[(-1)]
            lastlen = lastcharset.encoded_header_len(lastchunk)

        return self._encode_chunks(newchunks, maxlinelen)


def _split_ascii(s, firstlen, restlen, continuation_ws, splitchars):
    lines = []
    maxlen = firstlen
    for line in s.splitlines():
        line = line.lstrip()
        if len(line) < maxlen:
            lines.append(line)
            maxlen = restlen
            continue
        for ch in splitchars:
            if ch in line:
                break
        else:
            lines.append(line)
            maxlen = restlen
            continue

        cre = re.compile('%s\\s*' % ch)
        if ch in ';,':
            eol = ch
        else:
            eol = ''
        joiner = eol + ' '
        joinlen = len(joiner)
        wslen = len(continuation_ws.replace('\t', SPACE8))
        this = []
        linelen = 0
        for part in cre.split(line):
            curlen = linelen + max(0, len(this) - 1) * joinlen
            partlen = len(part)
            onfirstline = not lines
            if ch == ' ' and onfirstline and len(this) == 1 and fcre.match(this[0]):
                this.append(part)
                linelen += partlen
            elif curlen + partlen > maxlen:
                if this:
                    lines.append(joiner.join(this) + eol)
                if partlen > maxlen and ch != ' ':
                    subl = _split_ascii(part, maxlen, restlen, continuation_ws, ' ')
                    lines.extend(subl[:-1])
                    this = [subl[(-1)]]
                else:
                    this = [
                     part]
                linelen = wslen + len(this[(-1)])
                maxlen = restlen
            else:
                this.append(part)
                linelen += partlen

        if this:
            lines.append(joiner.join(this))

    return lines


def _binsplit(splittable, charset, maxlinelen):
    i = 0
    j = len(splittable)
    while i < j:
        m = i + j + 1 >> 1
        chunk = charset.from_splittable(splittable[:m], True)
        chunklen = charset.encoded_header_len(chunk)
        if chunklen <= maxlinelen:
            i = m
        else:
            j = m - 1

    first = charset.from_splittable(splittable[:i], False)
    last = charset.from_splittable(splittable[i:], False)
    return (first, last)