# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/nas.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 795 bytes
"""Amcrest NAS."""

class Nas(object):
    __doc__ = 'Amcrest methods to handle NAS.'

    @property
    def nas_information(self):
        """Return NAS information."""
        ret = self.command('configManager.cgi?action=getConfig&name=NAS')
        return ret.content.decode('utf-8')