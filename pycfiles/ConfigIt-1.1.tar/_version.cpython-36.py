# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/configirl-project/configirl/_version.py
# Compiled at: 2020-04-19 12:45:09
# Size of source mod 2**32: 195 bytes
import os, sys
sys.path.append(os.path.dirname(__file__))
from __init__ import __version__
if __name__ == '__main__':
    print(__version__)