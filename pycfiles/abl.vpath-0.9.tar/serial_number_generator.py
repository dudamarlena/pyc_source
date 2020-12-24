# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/errorreporter/util/serial_number_generator.py
# Compiled at: 2012-01-03 09:44:45
__doc__ = '\nCreates a human-readable identifier, using numbers and digits,\navoiding ambiguous numbers and letters.  hash_identifier can be used\nto create compact representations that are unique for a certain string\n(or concatenation of strings)\n'
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

good_characters = '23456789abcdefghjkmnpqrtuvwxyz'
base = len(good_characters)

def make_identifier(number):
    """
    Encodes a number as an identifier.
    """
    if not isinstance(number, (int, long)):
        raise ValueError('You can only make identifiers out of integers (not %r)' % number)
    if number < 0:
        raise ValueError('You cannot make identifiers out of negative numbers: %r' % number)
    result = []
    while number:
        next = number % base
        result.append(good_characters[next])
        number = number / base

    return ('').join(result)


def hash_identifier(s, length, pad=True, hasher=md5, prefix='', group=None, upper=False):
    """
    Hashes the string (with the given hashing module), then turns that
    hash into an identifier of the given length (using modulo to
    reduce the length of the identifier).  If ``pad`` is False, then
    the minimum-length identifier will be used; otherwise the
    identifier will be padded with 0's as necessary.

    ``prefix`` will be added last, and does not count towards the
    target length.  ``group`` will group the characters with ``-`` in
    the given lengths, and also does not count towards the target
    length.  E.g., ``group=4`` will cause a identifier like
    ``a5f3-hgk3-asdf``.  Grouping occurs before the prefix.
    """
    if not callable(hasher):
        hasher = hasher.new
    if length > 26 and hasher is md5:
        raise ValueError, 'md5 cannot create hashes longer than 26 characters in length (you gave %s)' % length
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    h = hasher(str(s))
    bin_hash = h.digest()
    modulo = base ** length
    number = 0
    for c in list(bin_hash):
        number = (number * 256 + ord(c)) % modulo

    ident = make_identifier(number)
    if pad:
        ident = good_characters[0] * (length - len(ident)) + ident
    if group:
        parts = []
        while ident:
            parts.insert(0, ident[-group:])
            ident = ident[:-group]

        ident = ('-').join(parts)
    if upper:
        ident = ident.upper()
    return prefix + ident


__test__ = {'make_identifier': "\n    >>> make_identifier(0)\n    ''\n    >>> make_identifier(1000)\n    'c53'\n    >>> make_identifier(-100)\n    Traceback (most recent call last):\n        ...\n    ValueError: You cannot make identifiers out of negative numbers: -100\n    >>> make_identifier('test')\n    Traceback (most recent call last):\n        ...\n    ValueError: You can only make identifiers out of integers (not 'test')\n    >>> make_identifier(1000000000000)\n    'c53x9rqh3'\n    ", 
   'hash_identifier': "\n    >>> hash_identifier(0, 5)\n    'cy2dr'\n    >>> hash_identifier(0, 10)\n    'cy2dr6rg46'\n    >>> hash_identifier('this is a test of a long string', 5)\n    'awatu'\n    >>> hash_identifier(0, 26)\n    'cy2dr6rg46cx8t4w2f3nfexzk4'\n    >>> hash_identifier(0, 30)\n    Traceback (most recent call last):\n        ...\n    ValueError: md5 cannot create hashes longer than 26 characters in length (you gave 30)\n    >>> hash_identifier(0, 10, group=4)\n    'cy-2dr6-rg46'\n    >>> hash_identifier(0, 10, group=4, upper=True, prefix='M-')\n    'M-CY-2DR6-RG46'\n    "}
if __name__ == '__main__':
    import doctest
    doctest.testmod()