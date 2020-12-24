# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/portletmanager/footer/interfaces.py
# Compiled at: 2009-10-06 10:29:36
from plone.portlets.interfaces import IPortletManager

class IFooter(IPortletManager):
    """ Portlet manager that is rendered in page footer

    Register a portlet for IFooter if it is applicable to page footer.
    """
    __module__ = __name__