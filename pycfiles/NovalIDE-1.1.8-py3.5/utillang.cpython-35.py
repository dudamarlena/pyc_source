# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/utillang.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 4467 bytes
import os, sys, tempfile
try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin

import xml.sax.saxutils as saxutils, noval.util.parser as parser
PY2WEB_codepages = {'cp1251': 'CP-1251', 
 'koi8_r': 'KOI8-R'}

def evalXPath(xpath, data, specialEntries=None):
    codeStr = parser.xpathToCode(xpath)
    return evalCode(codeStr, data, specialEntries)


def evalCode(codeStr, data, specialEntries=None):
    if isinstance(data, ObjAsDict):
        namespace = data
    else:
        if isinstance(data, dict):
            namespace = dict(data)
        else:
            namespace = ObjAsDict(data)
    if specialEntries:
        for key, value in specialEntries.items():
            namespace.addSpecialEntry(key, value)

    return eval(codeStr, {}, namespace)


def deriveCharset():
    charset = None
    encodingString = sys.getdefaultencoding()
    if encodingString != 'ascii':
        charset = PY2WEB_codepages.get(encodingString.lower())
        if charset == None:
            charset = encodingString
    return charset


def toUTF8(value):
    """
    Converts all unicode and non-string values to utf-8.
    This assumes string instances are already encoded in utf-8.
    Note that us-ascii is a subset of utf-8.
    """
    if isinstance(value, unicode):
        return value.encode('utf-8')
    return str(value)


def toUnicode(value):
    """
    Converts all strings non-string values to unicode.
    This assumes string instances are encoded in utf-8.
    Note that us-ascii is a subset of utf-8.
    """
    if not isinstance(value, unicode):
        if not isinstance(value, str):
            return unicode(value)
        return unicode(value, 'utf-8')
    return value


def getSystemTempDir():
    return tempfile.gettempdir()


def getEnvVar(name, defaultVal=None):
    if os.environ.has_key(name):
        return os.environ[name]
    return defaultVal


class ObjAsDict(DictMixin):
    __doc__ = '\n    Passing this to eval as the local variables dictionary allows the\n    evaluated code to access properties in the wrapped object\n    '

    def __init__(self, obj):
        self.obj = obj
        self.specialEntries = {}

    def __getitem__(self, key):
        try:
            return getattr(self.obj, key)
        except AttributeError as e:
            if self.specialEntries.has_key(key):
                return self.specialEntries[key]
            raise KeyError(e.args)

    def __setitem__(self, key, item):
        setattr(self.obj, key, item)

    def __delitem__(self, key):
        delattr(self.obj, key)

    def keys(self):
        ret = []
        for i in list(dir(self.obj) + self.specialEntries.keys()):
            if not i == '__doc__':
                if i == '__module__':
                    pass
                elif i not in ret:
                    ret.append(i)

        return ret

    def addSpecialEntry(self, key, value):
        self.specialEntries[key] = value


saxXMLescapeDoubleQuote = {'"': '&quot;'}
saxXMLescapesAllQuotes = {'"': '&quot;', "'": '&#039;'}
saxXMLunescapes = {'&quot;': '"', '&#039;': "'"}

def escape(data, extraEscapes=None):
    """Escape ', ", &, <, and > in a string of data.

    Basically, everything that saxutils.escape does (and this calls that, at
    least for now), but with " and ' added as well.

    TODO: make this faster; saxutils.escape() is really slow
    """
    global saxXMLescapeDoubleQuote
    if extraEscapes == None:
        extraEscapes = saxXMLescapeDoubleQuote
    return saxutils.escape(data, extraEscapes)


def unescape(data):
    """Unescape ', ", &, <, and > in a string of data.

    Basically, everything that saxutils.unescape does (and this calls that, at
    least for now), but with " and ' added as well.

    TODO: make this faster; saxutils.unescape() is really slow
    """
    global saxXMLunescapes
    return saxutils.unescape(data, saxXMLunescapes)


# global saxXMLescapesAllQuotes ## Warning: Unused global