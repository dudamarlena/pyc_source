# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/LineSplit.py
# Compiled at: 2008-10-19 12:19:52
from PureTransformer import PureTransformer

class LineSplit(PureTransformer):
    """Split each message into its separate lines and send them on as separate messages"""

    def processMessage(self, msg):
        splitmsg = msg.split('\n')
        for line in splitmsg:
            self.send(line, 'outbox')


__kamaelia_components__ = (LineSplit,)