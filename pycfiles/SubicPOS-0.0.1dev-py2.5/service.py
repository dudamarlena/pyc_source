# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subicpos/controllers/service.py
# Compiled at: 2008-05-21 22:43:52
import logging
from subicpos.lib.base import *
from transaction import TransactionController
log = logging.getLogger(__name__)

class ServiceController(TransactionController):

    def _list_query(self):
        self.query = model.Session.query(self.table).order_by(self.table.id.desc())
        self.query = self.query.filter_by(type=2)

    def render_edit(self):
        return render('/service/edit.mako')

    def _save_custom(self, params):
        if g.branch_id > 0:
            params['branch'] = g.branch_id
        params['type'] = 2
        return params