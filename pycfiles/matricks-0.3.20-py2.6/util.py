# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/matricks/util.py
# Compiled at: 2011-04-10 17:27:34
from matricks import Matricks

def convert(old_m):
    """Convert pre 0.2.14 matricks instances (ala restored from pickle) to
new format.
"""
    data = list(old_m._data)
    data.insert(0, old_m.getLabels())
    return Matricks(data)