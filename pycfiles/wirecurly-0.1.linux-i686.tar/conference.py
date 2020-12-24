# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/dialplan/applications/conference.py
# Compiled at: 2014-01-08 15:34:56
from wirecurly.dialplan.applications import ApplicationBase

class Conference(ApplicationBase):
    """The conference application"""

    def __init__(self, conf_name, profile='default'):
        super(Conference, self).__init__('conference')
        self.conf_name = conf_name
        self.profile = profile
        self.pin = None
        return

    @property
    def data(self):
        """
                        Getter for data so we can properly manipulate application configuration
                """
        if self.pin is None:
            return ('{0}@{1}').format(self.conf_name, self.profile)
        else:
            return ('{0}@{1}+{2}').format(self.conf_name, self.profile, self.pin)
            return

    def setPin(self, pin):
        """
                        Set conference PIN
                """
        self.pin = pin

    def clearPin(self):
        """
                        Clear conference PIN
                """
        self.pin = None
        return