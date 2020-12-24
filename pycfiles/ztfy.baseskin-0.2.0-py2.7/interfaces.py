# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/tal/interfaces.py
# Compiled at: 2014-03-15 19:45:12
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class ISkinTalesAPI(Interface):
    """'skin:' TALES namespace interface"""

    def presentation(self):
        """Get presentation of adapted context"""
        pass


class IContentMetasAPI(Interface):
    """'metas' TALES namespace interface"""

    def items(self):
        """Get list of metas headers"""
        pass

    def render(self):
        """Get content metas headers"""
        pass