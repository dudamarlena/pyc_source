# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/contact.py
# Compiled at: 2008-06-20 03:40:59
import logging
from pycrud.lib.base import *
log = logging.getLogger(__name__)

class ContactChildList(ChildList):

    def __init__(self, parent, field, details):
        self.parent = parent
        self.field = field
        self.details = details
        self.table = details['table']
        self.columns = details['columns']
        self.children = getattr(parent, field)

    def save_custom(self, kw):
        if not kw.has_key('number'):
            return
        for prefix in g.prefixes:
            kw['number'] = h.strip_prefix(kw['number']).replace(' ', '')

    def save(self, id=None, **kw):
        self.save_custom(kw)
        if id is None:
            entry = self.table(**kw)
            self.children.append(entry)
            model.Session.save_or_update(self.parent)
        else:
            entry = model.get(self.table, id)
            for (k, v) in kw.iteritems():
                setattr(entry, k, v)

            model.Session.save_or_update(entry)
        return


class ContactController(ListController):
    table = model.Contact
    children = dict(phone=dict(table=model.Phone, columns=('number', )), address=dict(table=model.Address, columns=('address', )))

    def _save_children(self, entry, **kw):
        for (field, children) in self.children.iteritems():
            child_list = ContactChildList(entry, field, children)
            child_list.multi_save(**kw)

        return entry