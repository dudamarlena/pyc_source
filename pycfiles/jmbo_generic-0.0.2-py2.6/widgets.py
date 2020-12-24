# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/generic/widgets.py
# Compiled at: 2011-09-27 09:30:07
import types
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.datastructures import MultiValueDict

class SelectCommaWidget(CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        if not isinstance(value, types.ListType):
            value = value.split(',')
        return super(SelectCommaWidget, self).render(name, value, attrs=attrs, choices=choices)

    def value_from_datadict(self, data, files, name):
        result = super(SelectCommaWidget, self).value_from_datadict(data, files, name)
        if isinstance(result, types.ListType):
            return (',').join(result)
        return result