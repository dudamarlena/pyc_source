# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/browser/admin/migrate.py
# Compiled at: 2008-09-03 11:15:24
import transaction
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICategory

class MigrateView(BrowserView):
    """
    """
    __module__ = __name__

    def migrate(self):
        """
        """
        import pdb
        pdb.set_trace()