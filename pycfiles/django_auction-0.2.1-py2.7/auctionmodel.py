# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auction/models/auctionmodel.py
# Compiled at: 2013-04-22 07:14:52
import importlib
from django.conf import settings
from auction.utils.loader import load_class
AUCTION_AUCTION_MODEL = getattr(settings, 'AUCTION_AUCTION_MODEL', 'auction.models.defaults.Auction')
Auction = load_class(AUCTION_AUCTION_MODEL, 'AUCTION_AUCTION_MODEL')