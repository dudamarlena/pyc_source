# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/properties_as_fields.py
# Compiled at: 2013-04-11 17:47:52
import math
from camelot.admin.object_admin import ObjectAdmin
from camelot.view.controls import delegates

class Coordinate(object):

    def __init__(self, x=0, y=0):
        self.id = 1
        self.x = x
        self.y = y

    @property
    def r(self):
        return math.sqr(self.x ** 2, self.y ** 2)

    class Admin(ObjectAdmin):
        form_display = [
         'x', 'y', 'r']
        field_attributes = dict(x=dict(delegate=delegates.FloatDelegate, editable=True), y=dict(delegate=delegates.FloatDelegate, editable=True), r=dict(delegate=delegates.FloatDelegate))