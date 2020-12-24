# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/browser/payment_method.py
# Compiled at: 2008-06-20 09:36:52
from Products.Five.browser import BrowserView

class PaymentMethodView(BrowserView):
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