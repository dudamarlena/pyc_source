# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/z2.py
# Compiled at: 2006-09-22 15:28:54
""" Zope2 support

$Id: z2.py,v 1.1 2006/09/22 19:28:54 tseaver Exp $
"""
from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import Implicit
from Globals import InitializeClass
from pushpage.browser import PushPage
from pushpage.browser import PushPageFactory

class Z2PushPage(Implicit, PushPage):
    """ Zope2 wrapper.
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    security.declareObjectPublic()
    index_html = None


InitializeClass(Z2PushPage)

class Z2PushPageFactory(PushPageFactory):
    __module__ = __name__
    page_class = Z2PushPage