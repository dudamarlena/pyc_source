# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/password.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1375 bytes
"""PyAMS_form.browser.password module

Password widget implementation.
"""
from zope.interface import implementer_only
from zope.schema.interfaces import IPassword
from pyams_form.browser.text import TextWidget
from pyams_form.interfaces.widget import IPasswordWidget, IFieldWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@implementer_only(IPasswordWidget)
class PasswordWidget(TextWidget):
    __doc__ = 'Input type password widget implementation.'
    klass = 'password-widget'
    css = 'password'


@adapter_config(required=(IPassword, IFormLayer), provides=IFieldWidget)
def PasswordFieldWidget(field, request):
    """IFieldWidget factory for IPasswordWidget."""
    return FieldWidget(field, PasswordWidget(request))