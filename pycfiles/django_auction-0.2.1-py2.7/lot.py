# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auction/models/lot.py
# Compiled at: 2013-04-22 04:27:13
import importlib
from django.conf import settings
from auction.utils.loader import load_class
LOT_MODEL = getattr(settings, 'AUCTION_LOT_MODEL', 'auction.models.defaults.Lot')
Lot = load_class(LOT_MODEL, 'AUCTION_LOT_MODEL')