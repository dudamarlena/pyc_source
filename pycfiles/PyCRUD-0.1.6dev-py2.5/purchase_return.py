# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/purchase_return.py
# Compiled at: 2008-06-20 02:48:54
import logging
from pycrud.lib.base import *
from transaction import TransactionController
log = logging.getLogger(__name__)

class PurchaseReturnController(TransactionController):

    def _list_query(self):
        self.query = model.Session.query(self.table).order_by(self.table.id.desc())
        self.query = self.query.filter_by(type=6)

    def render_edit(self):
        return render('/purchase_return/edit.mako')