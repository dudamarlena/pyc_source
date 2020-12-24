# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/taxes/browser/tax.py
# Compiled at: 2008-09-03 11:15:45
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import INumberConverter

class TaxView(BrowserView):
    """
    """
    __module__ = __name__

    def getCriteria(self):
        """
        """
        result = []
        for (index, criteria) in enumerate(self.context.objectValues()):
            if index % 2 == 0:
                klass = 'odd'
            else:
                klass = 'even'
            result.append({'title': criteria.Title(), 'url': criteria.absolute_url(), 'value': criteria.getValue(), 'class': klass})

        return result

    def getRate(self):
        """
        """
        nc = queryUtility(INumberConverter)
        return nc.floatToTaxString(self.context.getRate())