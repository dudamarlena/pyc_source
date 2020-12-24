# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/fields_with_tooltips.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.object_admin import ObjectAdmin
from camelot.view.controls import delegates

def dynamic_tooltip_x(coordinate):
    return 'The <b>x</b> value of the coordinate, now set to %s' % coordinate.x


def dynamic_tooltip_y(coordinate):
    return 'The <b>y</b> value of the coordinate, now set to %s' % coordinate.y


class Coordinate(object):

    def __init__(self):
        self.id = 1
        self.x = 0.0
        self.y = 0.0

    class Admin(ObjectAdmin):
        form_display = [
         'x', 'y']
        field_attributes = dict(x=dict(delegate=delegates.FloatDelegate, tooltip=dynamic_tooltip_x), y=dict(delegate=delegates.FloatDelegate, tooltip=dynamic_tooltip_y))
        form_size = (100, 100)