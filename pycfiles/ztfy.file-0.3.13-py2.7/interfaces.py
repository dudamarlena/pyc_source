# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/tal/interfaces.py
# Compiled at: 2012-06-20 11:31:01
from zope.interface import Interface

class IImageDisplayTalesAPI(Interface):
    """'display:' TALES namespace interface"""

    def adapter(self):
        """Get display adapter"""
        pass