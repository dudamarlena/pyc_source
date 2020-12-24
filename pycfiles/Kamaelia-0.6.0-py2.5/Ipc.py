# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/IPC.py
# Compiled at: 2008-10-19 12:19:52
from Axon.Ipc import producerFinished, notify

class socketShutdown(producerFinished):
    """Message to indicate that the network connection has been closed."""
    pass


class serverShutdown(producerFinished):
    """Message to indicate that the server should shutdown"""
    pass


class newCSA(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA, sock=None):
        super(newCSA, self).__init__(caller, CSA)
        self.sock = sock

    def handlesWriting(self):
        return True


class shutdownCSA(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(shutdownCSA, self).__init__(caller, CSA)

    def shutdown(self):
        return True


class newServer(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(newServer, self).__init__(caller, CSA)

    def handlesWriting(self):
        return False


class newWriter(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
    will return the CSA."""

    def __init__(self, caller, CSA):
        super(newWriter, self).__init__(caller, CSA)
        self.hasOOB = False


class newReader(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(newReader, self).__init__(caller, CSA)
        self.hasOOB = False


class newExceptional(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(newExceptional, self).__init__(caller, CSA)
        self.hasOOB = False


class removeReader(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(removeReader, self).__init__(caller, CSA)
        self.hasOOB = False


class removeWriter(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(removeWriter, self).__init__(caller, CSA)
        self.hasOOB = False


class removeExceptional(notify):
    """Helper class to notify of new CSAs as they are created.  newCSA.object
   will return the CSA."""

    def __init__(self, caller, CSA):
        super(removeExceptional, self).__init__(caller, CSA)
        self.hasOOB = False