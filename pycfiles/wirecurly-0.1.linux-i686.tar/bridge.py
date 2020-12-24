# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/dialplan/applications/bridge.py
# Compiled at: 2014-01-08 15:34:56
from wirecurly.dialplan.applications import ApplicationBase

class Bridge(ApplicationBase):
    """Bridge application"""

    def __init__(self, dialstring):
        super(Bridge, self).__init__('bridge')
        self.dialstring = dialstring

    @property
    def data(self):
        """
                        Data is the whole dialstring
                """
        return self.dialstring