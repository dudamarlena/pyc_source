# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/text.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 2579 bytes
"""PyAMS_form.browser.text module

This module provides default text widget.
"""
from zope.interface import implementer_only
from zope.schema.interfaces import IASCIILine, IBytesLine, IDate, IDatetime, IDecimal, IFloat, IId, IInt, ITextLine, ITime, ITimedelta, IURI
from pyams_form.browser.widget import HTMLTextInputWidget, add_field_class
from pyams_form.interfaces.widget import IFieldWidget, ITextWidget
from pyams_form.widget import FieldWidget, Widget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@implementer_only(ITextWidget)
class TextWidget(HTMLTextInputWidget, Widget):
    __doc__ = 'Input type text widget implementation.'
    klass = 'text-widget'
    css = 'text'
    value = ''

    def update(self):
        super(TextWidget, self).update()
        add_field_class(self)


@adapter_config(required=(IBytesLine, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IASCIILine, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(ITextLine, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IId, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IInt, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IFloat, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IDecimal, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IDate, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IDatetime, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(ITime, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(ITimedelta, IFormLayer), provides=IFieldWidget)
@adapter_config(required=(IURI, IFormLayer), provides=IFieldWidget)
def TextFieldWidget(field, request):
    """IFieldWidget factory for TextWidget."""
    return FieldWidget(field, TextWidget(request))