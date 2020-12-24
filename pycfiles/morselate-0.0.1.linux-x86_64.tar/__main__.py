# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/felipe/.virtualenvs/morselate/lib/python2.7/site-packages/morselate/__main__.py
# Compiled at: 2017-10-21 20:12:59
"""Main module to run morselate"""
import sys
from . import demorse, emorse
if __name__ == '__main__':
    if len(sys.argv) == 1 or '-h' in sys.argv:
        print '\nUsage: \ndecode [-e] MORSE\nYet another morse encoder/decoder!\n\n    -e  Encodes a text instead of decoding a morse\n        '
    if '-e' in sys.argv:
        print emorse(sys.argv[2:])
    print demorse(sys.argv[1:])