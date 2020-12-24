# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/tal/interfaces.py
# Compiled at: 2013-09-22 13:17:50
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class ISiteManagerTalesAPI(Interface):
    """'site:' TALES namespace interface"""

    def manager():
        """Get site manager parent of given context"""
        pass

    def presentation():
        """Get site manager presentation of given context"""
        pass


class IGoogleTalesAPI(Interface):
    """'google' TALES namespace interface"""

    def analytics():
        """Get site manager Google Analytics adapter"""
        pass

    def adsense():
        """Get site manager Google AdSense adapter"""
        pass