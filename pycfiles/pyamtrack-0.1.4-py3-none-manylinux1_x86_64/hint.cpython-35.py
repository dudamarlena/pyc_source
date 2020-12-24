# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/hint.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1526 bytes
__doc__ = 'PyAMS_form.hint module\n\nField title hint adapter implementation.\n'
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
    """FieldDescriptionAsHint"""

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