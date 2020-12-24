# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/htmlDecode.py
# Compiled at: 2019-09-22 10:12:27
"""This is a copy of the htmlDecode function in Webware.

@@TR: It implemented more efficiently.

"""
from Cheetah.Utils.htmlEncode import htmlCodesReversed

def htmlDecode(s, codes=htmlCodesReversed):
    """ Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>. It is the inverse of htmlEncode()."""
    for code in codes:
        s = s.replace(code[1], code[0])

    return s