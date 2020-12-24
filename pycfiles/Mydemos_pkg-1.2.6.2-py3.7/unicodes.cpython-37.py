# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\unicodes.py
# Compiled at: 2020-05-04 10:28:54
# Size of source mod 2**32: 601 bytes
"""do you want a full list of unicode?
try this:
from Mydemos_pkg.unicodes import unicode_1,unicode_2,BMP_plane2,make_unicode
make_unicode()
unicode_1 #BMP
unicode_2 #plane2
BMP_plane2 #all
"""
print('initilizing...')
unicode_1 = [0] * 65536
unicode_2 = [0] * 131072
BMP_plane2 = [0] * 131072
print('unicodes modules release')

def make_unicode():
    for x in range(65536):
        unicode_1[x] = chr(x)
        BMP_plane2[x] = chr(x)

    for x in range(65536):
        unicode_2[x + 65536] = chr(x + 65536)
        BMP_plane2[x + 65536] = chr(x + 65536)


import unicodedata
del unicodedata