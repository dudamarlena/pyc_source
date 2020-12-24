# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/table/TableClickListenersExample.py
# Compiled at: 2013-04-04 15:36:38
import re
from babel.numbers import format_currency
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Table
from muntjac.ui.window import Notification
from muntjac.ui.table import IHeaderClickListener, IFooterClickListener
from muntjac.util import defaultLocale

class TableClickListenersExample(VerticalLayout):
    CURRENCY_PATTERN = '([£$€])(\\d+(?:\\.\\d{2})?)'

    def __init__(self):
        super(TableClickListenersExample, self).__init__()
        dataSource = ExampleUtil.getOrderContainer()
        totalSum = 0.0
        for i in range(len(dataSource)):
            item = dataSource.getItem(dataSource.getIdByIndex(i))
            value = item.getItemProperty(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID).getValue()
            match = re.search(self.CURRENCY_PATTERN, str(value))
            if match is not None:
                amount = match.groups()[1]
                totalSum += float(amount)

        table = Table('', ExampleUtil.getOrderContainer())
        table.setColumnExpandRatio(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 1)
        table.setSortDisabled(True)
        table.setWidth('100%')
        table.setPageLength(6)
        table.setFooterVisible(True)
        table.setImmediate(True)
        table.setColumnFooter(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 'Total Price')
        l = defaultLocale()
        fc = format_currency(totalSum, currency='USD', locale=l).encode('utf-8')
        table.setColumnFooter(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID, fc)
        table.addListener(HeaderListener(self), IHeaderClickListener)
        table.addListener(FooterListener(self), IFooterClickListener)
        self.addComponent(table)
        return

    def showHeaderHelpText(self, column):
        """Shows some help text when clicking on the header

        @param column
        """
        notification = None
        if column == ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID:
            notification = Notification(str(column) + '<br>', 'The description describes the type of product that has been ordered.')
        elif column == ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID:
            notification = Notification(str(column) + '<br>', 'The item price is calculated by multiplying the unit price with the quantity.')
        elif column == ExampleUtil.ORDER_QUANTITY_PROPERTY_ID:
            notification = Notification(str(column) + '<br>', 'The quantity describes how many items has been ordered.')
        elif column == ExampleUtil.ORDER_UNITPRICE_PROPERTY_ID:
            notification = Notification(str(column) + '<br>', 'The unit price is how much a single items costs. Taxes included.')
        else:
            return
        self.getWindow().showNotification(notification)
        return

    def showFooterHelpText(self, column):
        """Shows a footer help text

        @param column
        """
        notification = Notification('Total Price<br>', 'The total price is calculated by summing every items item price together.')
        self.getWindow().showNotification(notification)


class HeaderListener(IHeaderClickListener):

    def __init__(self, c):
        self._c = c

    def headerClick(self, event):
        self._c.showHeaderHelpText(event.getPropertyId())


class FooterListener(IFooterClickListener):

    def __init__(self, c):
        self._c = c

    def footerClick(self, event):
        self._c.showFooterHelpText(event.getPropertyId())