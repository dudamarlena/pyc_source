# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auction/models/defaults.py
# Compiled at: 2013-04-22 07:14:09
from django.db import models
from django.utils.translation import ugettext_lazy as _
from auction.models.bases import BaseAuction, BaseAuctionLot, BaseBidBasket, BaseBidItem

class Auction(BaseAuction):

    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Auction')
        verbose_name_plural = _('Auctions')


class Lot(BaseAuctionLot):

    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Auction lot')
        verbose_name_plural = _('Auction lots')


class BidBasket(BaseBidBasket):

    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Bid basket')
        verbose_name_plural = _('Bid baskets')


class BidItem(BaseBidItem):

    class Meta:
        abstract = False
        app_label = 'auction'
        verbose_name = _('Bid item')
        verbose_name_plural = _('Bid items')