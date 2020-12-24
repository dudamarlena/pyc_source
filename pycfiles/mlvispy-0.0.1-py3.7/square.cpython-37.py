# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/jupyter_vis/square.py
# Compiled at: 2019-07-16 14:44:43
# Size of source mod 2**32: 327 bytes
from __future__ import print_function
from jupyter_react import Component

class Square(Component):
    module = 'Square'

    def __init__(self, **kwargs):
        (super(Square, self).__init__)(target_name='react.jupyter_vis', **kwargs)
        self.on_msg(self._handle_msg)

    def _handle_msg(self, msg):
        print(msg)