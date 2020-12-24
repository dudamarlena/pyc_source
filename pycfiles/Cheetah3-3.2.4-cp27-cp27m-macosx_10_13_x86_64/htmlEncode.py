# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/htmlEncode.py
# Compiled at: 2019-09-22 10:12:27
"""This is a copy of the htmlEncode function in Webware.

@@TR: It implemented more efficiently.

"""
htmlCodes = [
 [
  '&', '&amp;'],
 [
  '<', '&lt;'],
 [
  '>', '&gt;'],
 [
  '"', '&quot;']]
htmlCodesReversed = htmlCodes[:]
htmlCodesReversed.reverse()

def htmlEncode(s, codes=htmlCodes):
    """ Returns the HTML encoded version of the given string. This is useful to
    display a plain ASCII text string on a web page."""
    for code in codes:
        s = s.replace(code[0], code[1])

    return s