# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Ryan\Documents\GitHub\FoxDot\FoxDot\lib\Extensions\VRender\Sinsy.py
# Compiled at: 2018-08-29 05:13:03
# Size of source mod 2**32: 322 bytes
import sys, urllib

def download(output, wavPath):
    text = reduce(lambda accum, x: accum + x, output, '')
    index = text.find('./temp/') + len('./temp/')
    text = text[index:index + 40].split('.')[0]
    testfile = urllib.URLopener()
    testfile.retrieve('http://sinsy.sp.nitech.ac.jp/temp/' + text + '.wav', wavPath)