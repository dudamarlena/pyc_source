# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/SingleShot.py
# Compiled at: 2008-10-19 12:19:52
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess

class OneShot(Axon.Component.component):

    def __init__(self, msg=None):
        super(OneShot, self).__init__()
        self.msg = msg

    def main(self):
        self.send(self.msg, 'outbox')
        yield 1