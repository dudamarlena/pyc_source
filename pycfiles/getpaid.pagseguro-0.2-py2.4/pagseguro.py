# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/getpaid/pagseguro/pagseguro.py
# Compiled at: 2009-04-20 19:03:52
"""
"""
import urllib
from Products.CMFCore.utils import getToolByName
from zope import component
from zope import interface
from interfaces import IPagseguroStandardOptions, IPagseguroStandardProcessor
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces
_sites = {'real': 'pagseguro.uol.com.br', 'teste': 'pagseguro.uol.com.br'}

class PagseguroStandardProcessor(object):
    __module__ = __name__
    interface.implements(IPagseguroStandardProcessor)
    options_interface = IPagseguroStandardOptions

    def __init__(self, context):
        self.context = context

    def cart_post_button(self, order):
        options = IPagseguroStandardOptions(self.context)
        siteroot = getToolByName(self.context, 'portal_url').getPortalObject()
        manage_options = IGetPaidManagementOptions(siteroot)
        cartitems = []
        idx = 1
        _button_form = '<form target="pagseguro" method="post"\naction="https://pagseguro.uol.com.br/security/webpagamentos/webpagto.aspx">\n<input type="hidden" name="email_cobranca" value="%(merchant_id)s">\n<input type="hidden" name="encoding" value="utf-8">\n<input type="hidden" name="tipo" value="CP">\n<input type="hidden" name="moeda" value="BRL">\n<input type="hidden" name="ref_transacao" value="%(order_id)s"/>\n%(cart)s\n\n<input type="image" \nsrc="https://pagseguro.uol.com.br/Security/Imagens/btnfinalizaBR.jpg" \nname="submit" alt="Pague com PagSeguro - e rapido, gratis e seguro!">\n</form>\n\n'
        _button_cart = '<input type="hidden" name="item_descr_%(idx)s" value="%(item_name)s" />\n<input type="hidden" name="item_id_%(idx)s" value="%(item_number)s" />\n<input type="hidden" name="item_quant_%(idx)s" value="%(quantity)s" />\n<input type="hidden" name="item_valor_%(idx)s" value="%(amount)s" />\n<input type="hidden" name="item_peso_%(idx)s" value="%(weight)s" />\n\n'
        for item in order.shopping_cart.values():
            weight = getattr(item, 'weight', 0)
            v = _button_cart % {'idx': idx, 'item_name': item.name, 'item_number': item.product_code, 'quantity': item.quantity, 'amount': int(item.cost * 100), 'weight': int(weight * 1000)}
            cartitems.append(v)
            idx += 1

        siteURL = siteroot.absolute_url()
        formvals = {'merchant_id': options.merchant_id, 'cart': ('').join(cartitems), 'order_id': order.order_id, 'store_name': manage_options.store_name}
        return _button_form % formvals

    def capture(self, order, price):
        return GetPaidInterfaces.keys.results_async

    def authorize(self, order, payment):
        pass