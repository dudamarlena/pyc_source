# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/twocheckout/__init__.py
# Compiled at: 2015-10-07 15:24:39
seller_id = None
private_key = None
sandbox = False
base_url = 'https://api.2checkout.com/v2/'
sandbox_base_url = 'https://api-sandbox.2checkout.com/v2/'
from twocheckout.request import Request
from twocheckout.resources import Resource, Sale, Invoice, Item, Subscription, Refund, Customer, PaymentMethod, Address, Comment, Pagination
from twocheckout.error import TwoCheckoutError
from twocheckout.response import Response