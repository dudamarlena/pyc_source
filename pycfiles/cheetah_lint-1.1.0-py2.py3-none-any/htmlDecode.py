# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/htmlDecode.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = 'This is a copy of the htmlDecode function in Webware.\n\n@@TR: It implemented more efficiently.\n\n'
from Cheetah.Utils.htmlEncode import htmlCodesReversed

def htmlDecode(s, codes=htmlCodesReversed):
    """ Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>. It is the inverse of htmlEncode()."""
    for code in codes:
        s = s.replace(code[1], code[0])

    return s