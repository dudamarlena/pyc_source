# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hnc\forms\layout.py
# Compiled at: 2013-08-29 11:22:40
from hnc.forms.formfields import WrapField, NO_GRID, CombinedField

class Sequence(WrapField):

    def __init__(self, *fields):
        self.fields = fields

    def render(self, prefix, request, values, errors, view=None, grid=NO_GRID):
        html = ('').join([ field.render(prefix, request, values, errors, view, grid) if field else '' for field in self.fields ])
        return html


class BS3_NCOL(WrapField):

    def __init__(self, *fields):
        self.fields = fields

    def render(self, prefix, request, values, errors, view=None, grid=NO_GRID):
        html = ('').join([ ('<div class="col-sm-{0}">{1}</div>').format(12 / len(self.fields), field.render(prefix, request, values, errors, view, grid) if field else '') for field in self.fields
                         ])
        return ('<div class="row">{}</div>').format(html)