# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-shop-server/shop/sale/utils.py
# Compiled at: 2017-01-02 10:49:30
# Size of source mod 2**32: 377 bytes
from .models import Cart

def get_cart(request, cart_pk=None):
    if request.user.is_authenticated:
        customer = request.user.customer
        return Cart.objects.filter(customer=customer).first()
    customer = None
    try:
        return Cart.objects.get(customer=customer, pk=cart_pk)
    except Cart.DoesNotExist:
        return