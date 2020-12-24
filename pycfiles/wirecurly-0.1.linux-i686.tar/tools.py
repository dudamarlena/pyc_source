# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/dialplan/applications/tools.py
# Compiled at: 2014-01-08 15:34:56
from wirecurly.dialplan.applications import ApplicationBase

class Answer(ApplicationBase):
    """The answer application"""

    def __init__(self):
        super(Answer, self).__init__('answer')

    @property
    def data(self):
        """
                        Answer does not need data, so return empty string.
                """
        return ''


class Sleep(ApplicationBase):
    """The sleep application"""

    def __init__(self, time_in_ms):
        super(Sleep, self).__init__('sleep')
        self.time_in_ms = time_in_ms

    @property
    def data(self):
        """
                        Sleep only needs to return the time to sleep in ms.
                """
        return self.time_in_ms