# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/submit.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1536 bytes
"""PyAMS_form.browser.submit module

This module provides form submit button widget.
"""
from zope.interface import implementer_only
from pyams_form.browser.button import ButtonWidget
from pyams_form.interfaces.button import IButton
from pyams_form.interfaces.widget import ISubmitWidget, IFieldWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@implementer_only(ISubmitWidget)
class SubmitWidget(ButtonWidget):
    __doc__ = 'Form submit button.'
    klass = 'submit-widget'
    css = 'submit'

    def json_data(self):
        data = super(SubmitWidget, self).json_data()
        data['type'] = 'submit'
        return data


@adapter_config(required=(IButton, IFormLayer), provides=IFieldWidget)
def SubmitFieldWidget(field, request):
    """Form submit button factory adapter"""
    submit = FieldWidget(field, SubmitWidget(request))
    submit.value = field.title
    return submit