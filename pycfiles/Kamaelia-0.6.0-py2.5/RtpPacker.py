# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/RTP/RtpPacker.py
# Compiled at: 2008-10-19 12:19:52
"""
RtpPacker Component
===================

Takes data from a preframer:

   * Creates an RTP Header Object
   * Uses the timestamp & sample count to generate an RTP timestamp

"""
from Axon.Component import component, scheduler

class RtpPacker(component):
    Inboxes = [
     'inbox']
    Outboxes = ['outbox']

    def __init__(self, label, looptimes, selfstart=0):
        super(RtpPacker, self).__init__()

    def initialiseComponent(self):
        return 1

    def mainBody(self):
        return 1

    def closeDownComponent(self):
        """closeDownComponent"""
        pass


__kamaelia_components__ = (
 RtpPacker,)
if __name__ == '__main__':
    pass