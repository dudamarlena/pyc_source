# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/PyArabic/araby.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\nArabic module\n\n@todo: normalize_spellerrors,normalize_hamza,normalize_shaping\n@todo: statistics calculator\n\n'
from araby_strip_functions import *
from araby_normalizers import *
from araby_predicates import *
from araby_constants import *
_arabic_range = None

def order(archar):
    """return Arabic letter order between 1 and 29.
    Alef order is 1, Yeh is 28, Hamza is 29.
    Teh Marbuta has the same ordre with Teh, 3.
    @param archar: arabic unicode char
    @type archar: unicode
    @return: arabic order.
    @rtype: integer;
    """
    if AlphabeticOrder.has_key(archar):
        return AlphabeticOrder[archar]
    else:
        return 0


def name(archar):
    """return Arabic letter name in arabic.
    Alef order is 1, Yeh is 28, Hamza is 29.
    Teh Marbuta has the same ordre with Teh, 3.
    @param archar: arabic unicode char
    @type archar: unicode
    @return: arabic name.
    @rtype: unicode;
    """
    if NAMES.has_key(archar):
        return NAMES[archar]
    else:
        return ''


def arabicrange():
    r"""return a list of arabic characteres .
    Return a list of characteres between \u060c to \u0652
    @return: list of arabic characteres.
    @rtype: unicode;
    
    >>> expected = map( lambda char: unichr( char ), range( 0x0600, 0x00653 ) )
    >>> arabicrange() == expected
    True
    >>> arabicrange() == expected
    True
    """
    if _arabic_range:
        return _arabic_range
    else:
        return map(unichr, range(1536, 1619))