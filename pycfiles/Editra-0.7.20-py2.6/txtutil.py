# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/txtutil.py
# Compiled at: 2011-07-23 10:15:21
"""
Editra Business Model Library: Text Utilities

Utility functions for managing and working with text.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: txtutil.py 67991 2011-06-20 23:48:01Z CJP $'
__revision__ = '$Revision: 67991 $'
__all__ = [
 'IsUnicode', 'DecodeString']
import types

def IsUnicode(txt):
    """Is the given string a unicode string
    @param txt: object
    @return: bool

    """
    return isinstance(txt, types.UnicodeType)


def DecodeString(txt, enc):
    """Decode the given string with the given encoding,
    only attempts to decode if the given txt is not already Unicode
    @param txt: string
    @param enc: encoding 'utf-8'
    @return: unicode

    """
    if IsUnicode(txt):
        txt = txt.decode(enc)
    return txt