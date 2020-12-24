# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/sessions/manager.py
# Compiled at: 2010-04-23 04:51:20


class SessionManager(object):
    """
    The state of a client connecting to the system. 
    
    FIXME: this design is prone to race conditions
    """

    def __init__(self, client, backend):
        self.client = client
        self.backend = backend

    def restore(self):
        """
        Restore the current state from the backend
        """
        self.data = self.backend.restore(self.client)

    def save(self, deactivate=False):
        """
        Save the current state to the backend. Specify deactivate=True if you
        want to close this session for good.
        """
        self.backend.save(self.client, self.data)
        if deactivate:
            self.backend.deactivate(self.client)