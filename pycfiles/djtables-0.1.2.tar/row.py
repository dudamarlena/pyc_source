# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/adammck/projects/djtables/example/djtables/row.py
# Compiled at: 2010-06-17 15:35:44


class Row(object):

    def __init__(self, table, obj):
        self.table = table
        self.obj = obj

    def __getattr__(self, name):
        if hasattr(self.obj, name):
            val = getattr(self.obj, name)
        elif hasattr(self.obj, '__getitem__') and name in self.obj:
            val = self.obj[name]
        else:
            val = None
        return callable(val) and val() or val

    def __unicode__(self):
        return unicode(self.obj)

    def __iter__(self):
        for column in self.table._meta.columns:
            yield self.table.cell(column, self)

    def __len__(self):
        return len(self.table._meta.columns)