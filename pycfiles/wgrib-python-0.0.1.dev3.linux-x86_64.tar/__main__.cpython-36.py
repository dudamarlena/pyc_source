# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/envs/py36/lib/python3.6/site-packages/wgrib/__main__.py
# Compiled at: 2018-02-27 07:02:28
# Size of source mod 2**32: 110 bytes
import sys
try:
    from .wgrib2 import main
except ImportError:
    from .wgrib import main

main(sys.argv)