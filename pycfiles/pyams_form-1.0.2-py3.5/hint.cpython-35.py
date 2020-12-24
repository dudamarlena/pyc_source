# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/hint.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1526 bytes
"""PyAMS_form.hint module

Field title hint adapter implementation.
"""
from zope.interface import Interface
from zope.schema.interfaces import IField
from pyams_form.interfaces import IValue
from pyams_form.interfaces.form import IForm
from pyams_form.interfaces.widget import IWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@adapter_config(name='title', required=(
 Interface, IFormLayer, IForm, IField, IWidget), provides=IValue)
class FieldDescriptionAsHint:
    __doc__ = "Schema field description as widget's ```Title`` IValue adapter"

    def __init__(self, context, request, form, field, widget):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget

    def get(self):
        """Return the value"""
        if self.field.description:
            return self.field.description