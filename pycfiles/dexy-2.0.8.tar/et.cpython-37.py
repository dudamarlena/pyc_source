# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/datas/et.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 405 bytes
from dexy.data import Generic
import xml.etree.ElementTree as ET

class EtreeData(Generic):
    __doc__ = '\n    Expose etree method to query XML using ElementTree.\n    '
    aliases = ['etree']

    def etree(self):
        """
        Returns a tree root object.
        """
        if not hasattr(self, '_etree_root'):
            self._etree_root = ET.fromstring(self.data())
        return self._etree_root