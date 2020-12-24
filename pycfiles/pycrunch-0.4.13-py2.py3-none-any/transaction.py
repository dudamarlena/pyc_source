# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/transaction.py
# Compiled at: 2008-06-20 02:48:54
import logging
from pycrud.lib.base import *
from pycrud import model
log = logging.getLogger(__name__)

class TransactionController(ListController):
    table = model.Transaction
    parent = dict(area=dict(table=model.Area, column='name'), type=dict(table=model.TransType, column='name'), agent=dict(table=model.Agent, column='name'), customer=dict(table=model.Customer, column='name'), pay_type=dict(table=model.PayType, column='name'))
    children = dict(trans_item=dict(table=model.TransItem, columns=('item', 'qty',
                                                                    'price', 'received_qty'), parent=dict(item=dict(table=model.Item, column='code'))))
    prices = dict()
    total = 0

    def show_price(self):
        item_id = request.params['item']
        try:
            qty = float(request.params['qty'])
        except ValueError:
            qty = 0

        item = model.get(model.Item, item_id)
        try:
            item_price = item.price
        except AttributeError:
            item_price = 0

        c.cnt = request.params['cnt']
        c.child = 'trans_item'
        c.child_details = self.children[c.child]
        c.table = c.child_details['table']
        c.columns = c.child_details['columns']
        c.price = qty * item_price
        self.prices[c.cnt] = c.price
        return render('/transaction/show_price.mako')