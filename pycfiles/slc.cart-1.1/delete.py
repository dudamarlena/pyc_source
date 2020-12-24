# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/slc.cart/src/slc/cart/actions/delete.py
# Compiled at: 2012-11-05 02:30:55
"""A Cart Action for deleting all items listed in cart."""
from five import grok
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from slc.cart.interfaces import ICartAction
NAME = 'delete'
TITLE = 'Delete'
WEIGHT = 20

class DeleteAction(grok.Adapter):
    """Delete Action implementation that deletes items listed in cart."""
    grok.context(ISiteRoot)
    grok.provides(ICartAction)
    grok.name(NAME)
    name = NAME
    title = TITLE
    weight = WEIGHT

    def run(self):
        """Delete all items currently in cart and clear the cart's contents."""
        cart_view = self.context.restrictedTraverse('cart')
        request = self.context.REQUEST
        cart = cart_view.cart
        for obj_uuid in cart:
            obj = api.content.get(UID=obj_uuid)
            if obj is None:
                continue
            api.content.delete(obj)

        api.portal.show_message(message='All items in cart were successfully deleted.', request=request, type='info')
        cart_view.clear()
        return