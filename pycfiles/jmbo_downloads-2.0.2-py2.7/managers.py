# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/downloads/managers.py
# Compiled at: 2015-04-21 15:31:46
from jmbo.managers import PermittedManager

class VisibleManager(PermittedManager):

    def get_query_set(self, include_invisible=False):
        qs = super(VisibleManager, self).get_query_set()
        if not include_invisible:
            qs = qs.exclude(visible=False)
        return qs