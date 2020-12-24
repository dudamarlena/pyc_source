# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/textarea.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1767 bytes
"""PyAMS_form.browser.textarea module

This module provides textarea widget.
"""
from zope.interface import implementer_only
from zope.schema.interfaces import IASCII, IText
from pyams_form.browser.widget import HTMLTextAreaWidget, add_field_class
from pyams_form.interfaces.widget import IFieldWidget, ITextAreaWidget
from pyams_form.widget import FieldWidget, Widget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@implementer_only(ITextAreaWidget)
class TextAreaWidget(HTMLTextAreaWidget, Widget):
    __doc__ = 'Textarea widget implementation.'
    klass = 'textarea-widget'
    css = 'textarea'
    value = ''

    def update(self):
        super(TextAreaWidget, self).update()
        add_field_class(self)

    def json_data(self):
        data = super(TextAreaWidget, self).json_data()
        data['type'] = 'textarea'
        return data


@adapter_config(required=(IASCII, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IText, IFormLayer), provides=IFieldWidget)
def TextAreaFieldWidget(field, request):
    """IFieldWidget factory for TextWidget."""
    return FieldWidget(field, TextAreaWidget(request))