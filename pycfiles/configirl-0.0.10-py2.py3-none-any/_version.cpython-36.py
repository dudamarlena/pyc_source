# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/configirl-project/configirl/_version.py
# Compiled at: 2020-04-19 12:45:09
# Size of source mod 2**32: 195 bytes
import os, sys
sys.path.append(os.path.dirname(__file__))
from __init__ import __version__
if __name__ == '__main__':
    print(__version__)