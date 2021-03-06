# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/util/string24.py
# Compiled at: 2012-02-27 07:41:53
__doc__ = "A collection of string operations (most are no longer used).\n\nWarning: most of the code you see here isn't normally used nowadays.\nBeginning with Python 1.6, many of these functions are implemented as\nmethods on the standard string object. They used to be implemented by\na built-in module called strop, but strop is now obsolete itself.\n\nPublic module variables:\n\nwhitespace -- a string containing all characters considered whitespace\nlowercase -- a string containing all characters considered lowercase letters\nuppercase -- a string containing all characters considered uppercase letters\nletters -- a string containing all characters considered letters\ndigits -- a string containing all characters considered decimal digits\nhexdigits -- a string containing all characters considered hexadecimal digits\noctdigits -- a string containing all characters considered octal digits\npunctuation -- a string containing all characters considered punctuation\nprintable -- a string containing all characters considered printable\n\n"
whitespace = ' \t\n\r\x0b\x0c'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lowercase + uppercase
ascii_lowercase = lowercase
ascii_uppercase = uppercase
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
printable = digits + letters + punctuation + whitespace
l = map(chr, xrange(256))
_idmap = str('').join(l)
del l

def capwords(s, sep=None):
    """capwords(s, [sep]) -> string

    Split the argument into words using split, capitalize each
    word using capitalize, and join the capitalized words using
    join. Note that this replaces runs of whitespace characters by
    a single space.

    """
    return (sep or ' ').join([ x.capitalize() for x in s.split(sep) ])


_idmapL = None

def maketrans(fromstr, tostr):
    """maketrans(frm, to) -> string

    Return a translation table (a string of 256 bytes long)
    suitable for use in string.translate.  The strings frm and to
    must be of the same length.

    """
    global _idmapL
    if len(fromstr) != len(tostr):
        raise ValueError, 'maketrans arguments must have same length'
    if not _idmapL:
        _idmapL = map(None, _idmap)
    L = _idmapL[:]
    fromstr = map(ord, fromstr)
    for i in range(len(fromstr)):
        L[fromstr[i]] = tostr[i]

    return ('').join(L)


import re as _re

class _multimap:
    """Helper class for combining multiple mappings.

    Used by .{safe_,}substitute() to combine the mapping and keyword
    arguments.
    """

    def __init__(self, primary, secondary):
        self._primary = primary
        self._secondary = secondary

    def __getitem__(self, key):
        try:
            return self._primary[key]
        except KeyError:
            return self._secondary[key]


class _TemplateMetaclass(type):
    pattern = '\n    %(delim)s(?:\n      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters\n      (?P<named>%(id)s)      |   # delimiter and a Python identifier\n      {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier\n      (?P<invalid>)              # Other ill-formed delimiter exprs\n    )\n    '

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {'delim': _re.escape(cls.delimiter), 
               'id': cls.idpattern}
        cls.pattern = _re.compile(pattern, _re.IGNORECASE | _re.VERBOSE)


class Template:
    """A string class for supporting $-substitutions."""
    __metaclass__ = _TemplateMetaclass
    delimiter = '$'
    idpattern = '[_a-z][_a-z0-9]*'

    def __init__(self, template):
        self.template = template

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(('').join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' % (
         lineno, colno))

    def substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                val = mapping[named]
                return '%s' % val
            else:
                if mo.group('escaped') is not None:
                    return self.delimiter
                if mo.group('invalid') is not None:
                    self._invalid(mo)
                raise ValueError('Unrecognized named group in pattern', self.pattern)
                return

        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        def convert(mo):
            named = mo.group('named')
            if named is not None:
                try:
                    return '%s' % mapping[named]
                except KeyError:
                    return self.delimiter + named

            braced = mo.group('braced')
            if braced is not None:
                try:
                    return '%s' % mapping[braced]
                except KeyError:
                    return self.delimiter + '{' + braced + '}'

            if mo.group('escaped') is not None:
                return self.delimiter
            else:
                if mo.group('invalid') is not None:
                    return self.delimiter
                raise ValueError('Unrecognized named group in pattern', self.pattern)
                return

        return self.pattern.sub(convert, self.template)


index_error = ValueError
atoi_error = ValueError
atof_error = ValueError
atol_error = ValueError

def lower(s):
    """lower(s) -> string

    Return a copy of the string s converted to lowercase.

    """
    return s.lower()


def upper(s):
    """upper(s) -> string

    Return a copy of the string s converted to uppercase.

    """
    return s.upper()


def swapcase(s):
    """swapcase(s) -> string

    Return a copy of the string s with upper case characters
    converted to lowercase and vice versa.

    """
    return s.swapcase()


def strip(s, chars=None):
    """strip(s [,chars]) -> string

    Return a copy of the string s with leading and trailing
    whitespace removed.
    If chars is given and not None, remove characters in chars instead.
    If chars is unicode, S will be converted to unicode before stripping.

    """
    return s.strip(chars)


def lstrip(s, chars=None):
    """lstrip(s [,chars]) -> string

    Return a copy of the string s with leading whitespace removed.
    If chars is given and not None, remove characters in chars instead.

    """
    return s.lstrip(chars)


def rstrip(s, chars=None):
    """rstrip(s [,chars]) -> string

    Return a copy of the string s with trailing whitespace removed.
    If chars is given and not None, remove characters in chars instead.

    """
    return s.rstrip(chars)


def split(s, sep=None, maxsplit=-1):
    """split(s [,sep [,maxsplit]]) -> list of strings

    Return a list of the words in the string s, using sep as the
    delimiter string.  If maxsplit is given, splits at no more than
    maxsplit places (resulting in at most maxsplit+1 words).  If sep
    is not specified or is None, any whitespace string is a separator.

    (split and splitfields are synonymous)

    """
    return s.split(sep, maxsplit)


splitfields = split

def rsplit(s, sep=None, maxsplit=-1):
    """rsplit(s [,sep [,maxsplit]]) -> list of strings

    Return a list of the words in the string s, using sep as the
    delimiter string, starting at the end of the string and working
    to the front.  If maxsplit is given, at most maxsplit splits are
    done. If sep is not specified or is None, any whitespace string
    is a separator.
    """
    return s.rsplit(sep, maxsplit)


def join(words, sep=' '):
    """join(list [,sep]) -> string

    Return a string composed of the words in list, with
    intervening occurrences of sep.  The default separator is a
    single space.

    (joinfields and join are synonymous)

    """
    return sep.join(words)


joinfields = join

def index(s, *args):
    """index(s, sub [,start [,end]]) -> int

    Like find but raises ValueError when the substring is not found.

    """
    return s.index(*args)


def rindex(s, *args):
    """rindex(s, sub [,start [,end]]) -> int

    Like rfind but raises ValueError when the substring is not found.

    """
    return s.rindex(*args)


def count(s, *args):
    """count(s, sub[, start[,end]]) -> int

    Return the number of occurrences of substring sub in string
    s[start:end].  Optional arguments start and end are
    interpreted as in slice notation.

    """
    return s.count(*args)


def find(s, *args):
    """find(s, sub [,start [,end]]) -> in

    Return the lowest index in s where substring sub is found,
    such that sub is contained within s[start,end].  Optional
    arguments start and end are interpreted as in slice notation.

    Return -1 on failure.

    """
    return s.find(*args)


def rfind(s, *args):
    """rfind(s, sub [,start [,end]]) -> int

    Return the highest index in s where substring sub is found,
    such that sub is contained within s[start,end].  Optional
    arguments start and end are interpreted as in slice notation.

    Return -1 on failure.

    """
    return s.rfind(*args)


_float = float
_int = int
_long = long

def atof(s):
    """atof(s) -> float

    Return the floating point number represented by the string s.

    """
    return _float(s)


def atoi(s, base=10):
    """atoi(s [,base]) -> int

    Return the integer represented by the string s in the given
    base, which defaults to 10.  The string s must consist of one
    or more digits, possibly preceded by a sign.  If base is 0, it
    is chosen from the leading characters of s, 0 for octal, 0x or
    0X for hexadecimal.  If base is 16, a preceding 0x or 0X is
    accepted.

    """
    return _int(s, base)


def atol(s, base=10):
    """atol(s [,base]) -> long

    Return the long integer represented by the string s in the
    given base, which defaults to 10.  The string s must consist
    of one or more digits, possibly preceded by a sign.  If base
    is 0, it is chosen from the leading characters of s, 0 for
    octal, 0x or 0X for hexadecimal.  If base is 16, a preceding
    0x or 0X is accepted.  A trailing L or l is not accepted,
    unless base is 0.

    """
    return _long(s, base)


def ljust(s, width, *args):
    """ljust(s, width[, fillchar]) -> string

    Return a left-justified version of s, in a field of the
    specified width, padded with spaces as needed.  The string is
    never truncated.  If specified the fillchar is used instead of spaces.

    """
    return s.ljust(width, *args)


def rjust(s, width, *args):
    """rjust(s, width[, fillchar]) -> string

    Return a right-justified version of s, in a field of the
    specified width, padded with spaces as needed.  The string is
    never truncated.  If specified the fillchar is used instead of spaces.

    """
    return s.rjust(width, *args)


def center(s, width, *args):
    """center(s, width[, fillchar]) -> string

    Return a center version of s, in a field of the specified
    width. padded with spaces as needed.  The string is never
    truncated.  If specified the fillchar is used instead of spaces.

    """
    return s.center(width, *args)


def zfill(x, width):
    """zfill(x, width) -> string

    Pad a numeric string x with zeros on the left, to fill a field
    of the specified width.  The string x is never truncated.

    """
    if not isinstance(x, basestring):
        x = repr(x)
    return x.zfill(width)


def expandtabs(s, tabsize=8):
    """expandtabs(s [,tabsize]) -> string

    Return a copy of the string s with all tab characters replaced
    by the appropriate number of spaces, depending on the current
    column, and the tabsize (default 8).

    """
    return s.expandtabs(tabsize)


def translate(s, table, deletions=''):
    """translate(s,table [,deletions]) -> string

    Return a copy of the string s, where all characters occurring
    in the optional argument deletions are removed, and the
    remaining characters have been mapped through the given
    translation table, which must be a string of length 256.  The
    deletions argument is not allowed for Unicode strings.

    """
    if deletions:
        return s.translate(table, deletions)
    else:
        return s.translate(table + s[:0])


def capitalize(s):
    """capitalize(s) -> string

    Return a copy of the string s with only its first character
    capitalized.

    """
    return s.capitalize()


def replace(s, old, new, maxsplit=-1):
    """replace (str, old, new[, maxsplit]) -> string

    Return a copy of string str with all occurrences of substring
    old replaced by new. If the optional argument maxsplit is
    given, only the first maxsplit occurrences are replaced.

    """
    return s.replace(old, new, maxsplit)


try:
    from strop import maketrans, lowercase, uppercase, whitespace
    letters = lowercase + uppercase
except ImportError:
    pass