# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/slc.cart/src/slc/cart/actions/cut.py
# Compiled at: 2012-11-05 02:13:49
"""A Cart Action for deleting all items listed in cart."""
from five import grok
from OFS.CopySupport import _cb_encode
from OFS.CopySupport import cookie_path
from OFS.Moniker import Moniker
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
from slc.cart.interfaces import ICartAction
NAME = 'cut'
TITLE = 'Cut'
WEIGHT = 17

class CutAction(grok.Adapter):
    """Cut Action implementation that performs "cut" on the items in cart."""
    grok.context(ISiteRoot)
    grok.provides(ICartAction)
    grok.name(NAME)
    name = NAME
    title = TITLE
    weight = WEIGHT

    def run(self):
        """Cut all items currently in cart and add them to clipboard.

        The tricky part here is that the method that Plone uses
        (manage_cutObjects) was only ment to work on objects of the same
        parent. However, our use case allows cutting objects of different
        parents. Hence we need to go one level deeper and reimplement some
        stuff that manage_cutObjects does in our own way.

        """
        cart_view = self.context.restrictedTraverse('cart')
        request = self.context.REQUEST
        cart = cart_view.cart
        obj_list = []
        for obj_uuid in cart:
            obj = api.content.get(UID=obj_uuid)
            if obj is None:
                continue
            if obj.wl_isLocked():
                continue
            if not obj.cb_isMoveable():
                continue
            m = Moniker(obj)
            obj_list.append(m.dump())

        ct_data = (
         1, obj_list)
        ct_data = _cb_encode(ct_data)
        response = request.response
        path = ('{0}').format(cookie_path(request))
        response.setCookie('__cp', ct_data, path=path)
        request['__cp'] = ct_data
        api.portal.show_message(message=('{0} item(s) cut.').format(len(obj_list)), request=request, type='info')
        portal = api.portal.get()
        response.redirect(portal.absolute_url() + '/@@cart')
        return