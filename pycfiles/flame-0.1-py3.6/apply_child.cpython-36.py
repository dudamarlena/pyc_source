# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/children/apply_child.py
# Compiled at: 2018-06-21 06:48:46
# Size of source mod 2**32: 903 bytes
from flame.apply import Apply

class ApplyChild(Apply):

    def __init__(self, parameters, results):
        Apply.__init__(self, parameters, results)