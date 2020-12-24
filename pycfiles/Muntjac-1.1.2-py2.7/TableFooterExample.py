# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/table/TableFooterExample.py
# Compiled at: 2013-04-04 15:36:38
import re
from babel.numbers import format_currency
from muntjac.util import defaultLocale
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Table

class TableFooterExample(VerticalLayout):
    CURRENCY_PATTERN = '([£$€])(\\d+(?:\\.\\d{2})?)'

    def __init__(self):
        super(TableFooterExample, self).__init__()
        dataSource = ExampleUtil.getOrderContainer()
        totalSum = 0.0
        for i in range(len(dataSource)):
            item = dataSource.getItem(dataSource.getIdByIndex(i))
            value = item.getItemProperty(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID).getValue()
            match = re.search(self.CURRENCY_PATTERN, str(value))
            if match is not None:
                amount = match.groups()[1]
                totalSum += float(amount)

        table = Table('Order table', dataSource)
        table.setPageLength(6)
        table.setWidth('100%')
        table.setColumnAlignments([Table.ALIGN_LEFT, Table.ALIGN_RIGHT,
         Table.ALIGN_RIGHT, Table.ALIGN_RIGHT])
        table.setColumnExpandRatio(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 1)
        table.setFooterVisible(True)
        table.setColumnFooter(ExampleUtil.ORDER_DESCRIPTION_PROPERTY_ID, 'Total Price')
        l = defaultLocale()
        fc = format_currency(totalSum, currency='USD', locale=l).encode('utf-8')
        table.setColumnFooter(ExampleUtil.ORDER_ITEMPRICE_PROPERTY_ID, fc)
        self.addComponent(table)
        return