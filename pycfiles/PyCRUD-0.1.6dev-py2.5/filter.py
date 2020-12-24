# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/filter.py
# Compiled at: 2008-06-20 03:40:59
"""Filter Controller

AUTHOR: Emanuel Gardaya Calso

Last Modified:
    2008-04-04

"""
import logging
from pycrud.lib.base import *
log = logging.getLogger(__name__)

def get_labels():
    return model.Session.query(model.Label).order_by(model.Label.c.name)


class Property(object):

    def __init__(self, parent, field, db_tbl):
        self.parent = parent
        self.field = getattr(parent, field)
        self.table = db_tbl
        for entry in list(self.field):
            self.field.remove(entry)

    def add(self, c_id):
        entry = model.Session.query(self.table).get(c_id)
        self.field.append(entry)


class FilterController(ListController):
    table = model.Filter
    children = dict(action=dict(table=model.FilterAction, columns=('action', 'details')), condition=dict(table=model.FilterCondition, columns=('field',
                                                                                                                                               'condition')))
    properties = (
     (
      'label', 'name', model.Label),)

    def add_child(self):
        self._edit_child()
        if request.params['child'] == 'condition':
            return render('/filter/add_condition.mako')
        elif request.params['child'] == 'action':
            return render('/filter/add_action.mako')
        return render('/add_child.mako')

    def edit_child(self):
        self._edit_child()
        c.entry = model.get(c.table, request.params['c_id'])
        c.p_id = request.params['p_id']
        if request.params['child'] == 'condition':
            return render('/filter/edit_condition.mako')
        elif request.params['child'] == 'action':
            return render('/filter/edit_action.mako')
        return render('/edit_child.mako')