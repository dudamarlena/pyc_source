# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/Util/py3compat.py
# Compiled at: 2016-11-22 15:21:45
__doc__ = "Compatibility code for handling string/bytes changes from Python 2.x to Py3k\n\nIn Python 2.x, strings (of type ''str'') contain binary data, including encoded\nUnicode text (e.g. UTF-8).  The separate type ''unicode'' holds Unicode text.\nUnicode literals are specified via the u'...' prefix.  Indexing or slicing\neither type always produces a string of the same type as the original.\nData read from a file is always of '''str'' type.\n\nIn Python 3.x, strings (type ''str'') may only contain Unicode text. The u'...'\nprefix and the ''unicode'' type are now redundant.  A new type (called\n''bytes'') has to be used for binary data (including any particular\n''encoding'' of a string).  The b'...' prefix allows one to specify a binary\nliteral.  Indexing or slicing a string produces another string.  Slicing a byte\nstring produces another byte string, but the indexing operation produces an\ninteger.  Data read from a file is of '''str'' type if the file was opened in\ntext mode, or of ''bytes'' type otherwise.\n\nSince PyCrypto aims at supporting both Python 2.x and 3.x, the following helper\nfunctions are used to keep the rest of the library as independent as possible\nfrom the actual Python version.\n\nIn general, the code should always deal with binary strings, and use integers\ninstead of 1-byte character strings.\n\nb(s)\n    Take a text string literal (with no prefix or with u'...' prefix) and\n    make a byte string.\nbchr(c)\n    Take an integer and make a 1-character byte string.\nbord(c)\n    Take the result of indexing on a byte string and make an integer.\ntobytes(s)\n    Take a text string, a byte string, or a sequence of character taken from\n    a byte string and make a byte string.\n"
__revision__ = '$Id$'
import sys
if sys.version_info[0] == 2:
    from types import UnicodeType as _UnicodeType

    def b(s):
        return s


    def bchr(s):
        return chr(s)


    def bstr(s):
        return str(s)


    def bord(s):
        return ord(s)


    def tobytes(s):
        if isinstance(s, _UnicodeType):
            return s.encode('latin-1')
        else:
            return ('').join(s)


    def tostr(bs):
        return unicode(bs, 'latin-1')


    from StringIO import StringIO as BytesIO
else:

    def b(s):
        return s.encode('latin-1')


    def bchr(s):
        return bytes([s])


    def bstr(s):
        if isinstance(s, str):
            return bytes(s, 'latin-1')
        else:
            return bytes(s)


    def bord(s):
        return s


    def tobytes(s):
        if isinstance(s, bytes):
            return s
        else:
            if isinstance(s, str):
                return s.encode('latin-1')
            return bytes(s)


    def tostr(bs):
        return bs.decode('latin-1')


    from io import BytesIO