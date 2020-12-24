# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/z2.py
# Compiled at: 2006-09-22 15:28:54
__doc__ = ' Zope2 support\n\n$Id: z2.py,v 1.1 2006/09/22 19:28:54 tseaver Exp $\n'
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