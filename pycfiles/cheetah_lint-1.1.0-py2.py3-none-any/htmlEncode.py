# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/htmlEncode.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = 'This is a copy of the htmlEncode function in Webware.\n\n\n@@TR: It implemented more efficiently.\n\n'
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