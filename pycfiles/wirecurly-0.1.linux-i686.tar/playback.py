# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/dialplan/applications/playback.py
# Compiled at: 2014-01-08 15:34:56
from wirecurly.dialplan.applications import ApplicationBase

class Playback(ApplicationBase):
    """The playback application"""

    def __init__(self, filename):
        super(Playback, self).__init__('playback')
        self.filename = filename

    @property
    def data(self):
        """
                        Filename only returns the file to be played.
                        We cannot make checks of file existence unless we are on the local machine.
                """
        return self.filename