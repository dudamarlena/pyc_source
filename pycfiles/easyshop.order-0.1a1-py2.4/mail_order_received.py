# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/order/browser/mail_order_received.py
# Compiled at: 2008-09-03 11:15:08
from easyshop.order.browser.order_view import OrderView
from easyshop.core.interfaces import IInformationManagement
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IShopManagement

class MailOrderReceivedView(OrderView):
    """
    """
    __module__ = __name__

    def getNote(self):
        """Returns the note from the selected payment method.
        """
        customer = self.context.getCustomer()
        pm = IPaymentInformationManagement(customer)
        selected_payment_method = pm.getSelectedPaymentMethod()
        note = selected_payment_method.getNote()
        payment_url = self.context.absolute_url() + '/pay'
        note = note.replace('[payment-url]', payment_url)
        return note

    def getCancellationInstruction(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        im = IInformationManagement(shop)
        page = im.getInformationPage('rueckgabebelehrung')
        return page.getText()