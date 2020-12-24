# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/sales_order.py
# Compiled at: 2008-06-20 02:48:54
import logging
from pycrud.lib.base import *
from transaction import TransactionController
log = logging.getLogger(__name__)

class SalesOrderController(TransactionController):

    def _list_query(self):
        self.query = model.Session.query(self.table).order_by(self.table.id.desc())
        self.query = self.query.filter_by(type=1)

    def render_edit(self):
        return render('/sales_order/edit.mako')

    def _save_custom(self, params):
        if g.area_id > 0:
            params['area'] = g.area_id
        params['type'] = 1
        entry = model.Session.query(model.Inventory).filter_by(area=params['area']).filter_by(item=params['trans_item.item'])
        entry[0].qty -= int(params['trans_item.qty'])
        return params