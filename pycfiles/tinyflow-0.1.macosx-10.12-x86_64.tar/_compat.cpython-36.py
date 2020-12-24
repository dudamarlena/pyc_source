# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wursterk/code/tinyflow/venv/lib/python3.6/site-packages/tinyflow/_compat.py
# Compiled at: 2017-03-15 21:10:24
# Size of source mod 2**32: 216 bytes
"""Python 2 support."""
import itertools as it, sys
if sys.version_info.major == 2:
    map = it.imap
    filter = it.ifilter
else:
    map = map
    filter = filter