# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/fields_with_actions.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.object_admin import ObjectAdmin
from camelot.view.controls import delegates

class Coordinate(object):

    def __init__(self):
        self.id = 1
        self.x = 0.0
        self.y = 0.0

    def _get_x(self):
        return self.x

    def _set_x(self, x):
        self.x = x
        self.y = max(self.y, x)

    _x = property(_get_x, _set_x)

    class Admin(ObjectAdmin):
        form_display = [
         '_x', 'y']
        field_attributes = dict(_x=dict(delegate=delegates.FloatDelegate, name='x'), y=dict(delegate=delegates.FloatDelegate))
        form_size = (100, 100)