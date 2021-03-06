# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/nas.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 795 bytes
__doc__ = 'Amcrest NAS.'

class Nas(object):
    """Nas"""

    @property
    def nas_information(self):
        """Return NAS information."""
        ret = self.command('configManager.cgi?action=getConfig&name=NAS')
        return ret.content.decode('utf-8')