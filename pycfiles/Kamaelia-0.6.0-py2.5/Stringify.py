# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Stringify.py
# Compiled at: 2008-10-19 12:19:52
"""=======================
Convert Data to Strings
=======================

A simple component that takes data items and converts them to strings.

Example Usage
-------------

A simple pipeline::

    Pipeline( sourceOfNonStrings(),
              Stringify(),
              consumerThatWantsStrings(),
            ).activate()
            

How does it work?
-----------------

Send data items to this component's "inbox" inbox. They are converted to
strings using the str(...) function, and sent on out of the "outbox" outbox.

Anything sent to this component's "control" inbox is ignored.

This component does not terminate.
"""
from Axon.Component import component, scheduler

class Stringify(component):
    """   Stringify() -> new Stringify.
   
   A component that converts data items received on its "inbox" inbox to
   strings and sends them on out of its "outbox" outbox.
   """
    Inboxes = {'inbox': 'Data items to convert to string', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'Data items converted to strings', 'signal': 'NOT USED'}

    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Stringify, self).__init__()
        self.activate()

    def mainBody(self):
        """Main loop body."""
        if self.dataReady('inbox'):
            theData = self.recv('inbox')
            self.send(str(theData), 'outbox')
        return 1


__kamaelia_components__ = (
 Stringify,)