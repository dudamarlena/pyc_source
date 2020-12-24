# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/interfaces/Deleter.py
# Compiled at: 2016-03-23 14:50:19
from Interface import Interface
from wintx.errors import *

class Deleter(Interface):
    """Whacka"""

    def remove(self, query_dict):
        """Removes records from the database matching the query"""
        pass