# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/UnseenOnly.py
# Compiled at: 2008-10-19 12:19:52
"""====================
UnseenOnly component
====================

This component forwards on any messages it receives that it has not
seen before.

Example Usage
-------------

Lines entered into this setup will only be duplicated on screen the
first time they are entered::

    pipeline(
        ConsoleReader(),
        UnseenOnly(),
        ConsoleEchoer()
    ).run()

"""
from PureTransformer import PureTransformer

class UnseenOnly(PureTransformer):
    """    UnseenOnly() -> new UnseenOnly component.
    
    Send items to the "inbox" inbox. Any items not "seen" already will be
    forwarded out of the "outbox" outbox. Send the same thing two or more
    times and it will only be sent on the first time.
    """

    def __init__(self):
        super(UnseenOnly, self).__init__()
        self.seen = {}

    def processMessage(self, msg):
        if not self.seen.get(msg, False):
            self.seen[msg] = True
            return msg


__kamaelia_components__ = (UnseenOnly,)