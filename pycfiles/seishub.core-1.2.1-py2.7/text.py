# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\util\text.py
# Compiled at: 2010-12-23 17:42:44
import hashlib, locale, re

def isInteger(data):
    """
    Tests if the given string is an integer.
    """
    try:
        stripped = str(int(data))
    except:
        return False

    if data == stripped:
        return True
    return False


def getFirstSentence(text, maxlen=255):
    """
    Returns the text left of the first occurring dot and reduces the final 
    text to maxlen chars.
    """
    if not text:
        return ''
    if '.' not in text:
        return text[0:maxlen]
    text = text.split('.')
    text = text[0] + '.'
    return text[0:maxlen].strip()


def toUnicode(text, charset=None):
    """
    Convert a `str` object to an `unicode` object.

    If `charset` is given, we simply assume that encoding for the text,
    but we'll use the "replace" mode so that the decoding will always
    succeed.
    If `charset` is ''not'' specified, we'll make some guesses, first
    trying the UTF-8 encoding, then trying the locale preferred encoding,
    in "replace" mode. This differs from the `unicode` builtin, which
    by default uses the locale preferred encoding, in 'strict' mode,
    and is therefore prompt to raise `UnicodeDecodeError`s.

    Because of the "replace" mode, the original content might be altered.
    If this is not what is wanted, one could map the original byte content
    by using an encoding which maps each byte of the input to an unicode
    character, e.g. by doing `unicode(text, 'iso-8859-1')`.
    """
    if not isinstance(text, str):
        if isinstance(text, Exception):
            try:
                return unicode(text)
            except UnicodeError:
                return (' ').join([ toUnicode(arg) for arg in text.args ])

        return unicode(text)
    if charset:
        return unicode(text, charset, 'replace')
    try:
        return unicode(text, 'utf-8')
    except UnicodeError:
        return unicode(text, locale.getpreferredencoding(), 'replace')


def hash(text):
    """
    Returns a hash of the given string.
    """
    return hashlib.sha224(text).hexdigest()


def validate_id(str):
    """
    Validates a given ID.
    
    IDs have to be alphanumeric and start with a character.
    """
    id_pt = "^[A-Za-z0-9]       # leading character\n    [A-Za-z0-9_.-]*$              # alphanumeric or '_','.','-'\n    "
    if str is None:
        return
    else:
        str = str.encode('utf-8')
        re_id = re.compile(id_pt, re.VERBOSE)
        m = re_id.match(str)
        if not m:
            raise ValueError('Invalid id: %s' % str)
        return str


def to_uri(package_id, resourcetype_id):
    uri = '/' + package_id
    if resourcetype_id:
        uri += '/' + resourcetype_id
    return uri


def from_uri(uri):
    elements = uri.split('/')
    pid = elements[1]
    if len(elements) == 3:
        rid = None
        args = elements[2]
    else:
        rid = elements[2]
        args = elements[3]
    return (
     pid, rid, args)