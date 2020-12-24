# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\sftp.py
# Compiled at: 2018-08-27 17:21:06
import pysftp

class SFTPClient(pysftp.Connection):
    """Save the host name of a pysftp Connection"""

    def __init__(self, host, **kwargs):
        super(SFTPClient, self).__init__(host, **kwargs)
        self.host = host