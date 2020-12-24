# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/response.py
# Compiled at: 2008-06-20 03:40:59
import logging
from pycrud.lib.base import *
from sqlchemistry import Config, Environment
log = logging.getLogger(__name__)

class ResponseController(ListController):
    table = model.Response
    children = dict(argument=dict(table=model.ResponseArgument, columns=('priority',
                                                                         'field'), label='User Input'), default=dict(table=model.ResponseDefault, columns=('field',
                                                                                                                                                           'value')), value=dict(table=model.ResponseValue, columns=('priority',
                                                                                                                                                                                                                     'label',
                                                                                                                                                                                                                     'field'), label='Output'))

    def _get_custom_tables(self):
        self.conf = Config(g.custom_config)
        self.env = Environment(self.conf)
        tables = self.env.tables
        return tables

    def edit(self, id):
        self._dbg('edit')
        self._details(request.params['id'])
        c.custom_tables = self._get_custom_tables()
        return render('/response/edit.mako')

    def add(self):
        self._dbg('add')
        self._add()
        c.custom_tables = self._get_custom_tables()
        return render('/response/edit.mako')

    def add_child(self):
        self._edit_child()
        c.custom_tables = self._get_custom_tables()
        return render('/response/add_child.mako')

    def edit_child(self):
        self._edit_child()
        c.entry = model.get(c.table, request.params['c_id'])
        c.custom_tables = self._get_custom_tables()
        c.p_id = request.params['p_id']
        return render('/response/edit_child.mako')